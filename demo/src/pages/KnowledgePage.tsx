import React, { useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Search, Database, Play, Pause, Upload } from "lucide-react";
import { Input } from "@/components/ui/input";
import { GraphCanvas, darkTheme, lightTheme } from "reagraph";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import {
  fadeIn,
  slideUp,
  staggerChildren,
  pageTransition,
} from "@/lib/animations";
import { useTheme } from "@/lib/ThemeProvider";
import { useKnowledge } from "@/lib/KnowledgeProvider";

interface KnowledgeItem {
  subject: string;
  predicate: string;
  object: string;
  timestamp: string;
}

interface KnowledgeBase {
  name: string;
  path: string;
  data: KnowledgeItem[];
}

const KnowledgePage = () => {
  const { theme } = useTheme();
  const { knowledgeBases, setKnowledgeBases } = useKnowledge();
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedBase, setSelectedBase] = useState<KnowledgeBase | null>(null);
  const [cameraMode, setCameraMode] = useState<"orbit" | "rotate">("orbit");

  useEffect(() => {
    if (knowledgeBases.length === 0) {
      fetch("/data/user_knowledge.json")
        .then((response) => response.json())
        .then((data) => {
          setKnowledgeBases([
            {
              name: "User Knowledge",
              path: "/data/user_knowledge.json",
              data,
              enabled: true,
            },
          ]);
        });
    }
  }, [knowledgeBases.length, setKnowledgeBases]);

  const filteredBases = knowledgeBases.filter((base) =>
    base.name.toLowerCase().includes(searchTerm.toLowerCase()),
  );

  const nodes = selectedBase
    ? Array.from(
        new Set([
          ...selectedBase.data.map((k) => k.subject),
          ...selectedBase.data.map((k) => k.object),
        ]),
      ).map((label) => ({
        id: label,
        label,
      }))
    : [];

  const edges = selectedBase
    ? selectedBase.data.map((k, i) => ({
        id: `${k.subject}-${k.predicate}-${k.object}-${i}`,
        source: k.subject,
        target: k.object,
        label: k.predicate,
      }))
    : [];

  return (
    <motion.div
      className="p-6 h-screen flex flex-col"
      initial="initial"
      animate="animate"
      exit="exit"
      variants={fadeIn}
      transition={pageTransition}
    >
      <motion.h1 className="text-2xl font-bold mb-6" variants={slideUp}>
        Knowledge Bases
      </motion.h1>
      <motion.div
        className="grid grid-cols-[300px_1fr] gap-6 flex-1 min-h-0"
        variants={staggerChildren}
      >
        <motion.div variants={slideUp}>
          <Card className="p-4 h-full flex flex-col">
            <div className="space-y-4 flex-1">
              <div className="relative">
                <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Search knowledge bases..."
                  className="pl-8"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </div>
              <ScrollArea className="h-[calc(100vh-16rem)]">
                <motion.div className="space-y-2" variants={staggerChildren}>
                  {filteredBases.map((base, index) => (
                    <motion.div
                      key={index}
                      variants={slideUp}
                      className={`p-4 rounded-lg hover:bg-muted cursor-pointer ${selectedBase?.path === base.path ? "bg-muted" : ""}`}
                      onClick={() => setSelectedBase(base)}
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                    >
                      <div className="flex items-center gap-3">
                        <Database className="h-5 w-5 text-primary" />
                        <div>
                          <p className="font-medium">
                            {base.name === base.path
                              ? base.name
                                  .replace(/\.json$/, "")
                                  .replace(/_/g, " ")
                              : base.name}
                          </p>
                          <p className="text-xs text-muted-foreground">
                            {base.data.length} connections
                          </p>
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </motion.div>
              </ScrollArea>
            </div>
            <div className="mt-4 pt-4 border-t">
              <Input
                type="file"
                accept=".json"
                onChange={(e) => {
                  const file = e.target.files?.[0];
                  if (file) {
                    const reader = new FileReader();
                    reader.onload = (e) => {
                      const data = JSON.parse(e.target.result as string);
                      setKnowledgeBases((prev) => [
                        ...prev,
                        {
                          name: file.name,
                          path: file.name,
                          data,
                        },
                      ]);
                    };
                    reader.readAsText(file);
                  }
                }}
                className="hidden"
                id="knowledge-upload"
              />
              <Button
                variant="outline"
                onClick={() =>
                  document.getElementById("knowledge-upload")?.click()
                }
                className="w-full"
              >
                <Upload className="mr-2 h-4 w-4" />
                Upload Knowledge Base
              </Button>
            </div>
          </Card>
        </motion.div>

        <motion.div variants={slideUp}>
          <Card className="p-4 h-full relative overflow-hidden">
            {selectedBase ? (
              <motion.div
                className="absolute inset-0"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.2 }}
              >
                <div className="absolute top-2 right-2 z-10">
                  <Button
                    variant="outline"
                    size="icon"
                    onClick={() =>
                      setCameraMode((mode) =>
                        mode === "orbit" ? "rotate" : "orbit",
                      )
                    }
                  >
                    {cameraMode === "orbit" ? (
                      <Play className="h-4 w-4" />
                    ) : (
                      <Pause className="h-4 w-4" />
                    )}
                  </Button>
                </div>
                <GraphCanvas
                  cameraMode={cameraMode}
                  theme={theme === "dark" ? darkTheme : lightTheme}
                  edgeArrowPosition="end"
                  edgeInterpolation="curved"
                  sizingType="centrality"
                  nodes={nodes}
                  edges={edges}
                  labelType="auto"
                  layoutType="forceDirected3d"
                >
                  <directionalLight position={[0, 5, -4]} intensity={1} />
                </GraphCanvas>
              </motion.div>
            ) : (
              <div className="flex items-center justify-center h-full text-muted-foreground">
                Select a knowledge base to visualize its connections
              </div>
            )}
          </Card>
        </motion.div>
      </motion.div>
    </motion.div>
  );
};

export default KnowledgePage;
