import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useKnowledge } from "@/lib/KnowledgeProvider";
import { Card } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Database, Search, Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Switch } from "@/components/ui/switch";

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
  enabled: boolean;
}

const KnowledgeBase = () => {
  const { knowledgeBases, setKnowledgeBases } = useKnowledge();
  const [searchTerm, setSearchTerm] = useState("");
  const navigate = useNavigate();

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

  return (
    <Card className="p-4 h-full bg-background flex flex-col">
      <div className="space-y-4">
        <h3 className="font-semibold">Knowledge Bases</h3>
        <div className="relative">
          <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search knowledge bases..."
            className="pl-8"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <ScrollArea className="flex-1">
          <div className="space-y-2">
            {filteredBases.map((base, index) => (
              <div
                key={index}
                className="flex items-center gap-3 p-2 rounded-lg hover:bg-muted cursor-pointer"
              >
                <Database className="h-4 w-4 text-primary" />
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium">{base.name}</p>
                  <p className="text-xs text-muted-foreground">
                    {base.data.length} connections
                  </p>
                </div>
                <Switch
                  checked={base.enabled}
                  onCheckedChange={(checked) => {
                    setKnowledgeBases((prev) =>
                      prev.map((kb) =>
                        kb.path === base.path
                          ? { ...kb, enabled: checked }
                          : kb,
                      ),
                    );
                  }}
                />
              </div>
            ))}
          </div>
        </ScrollArea>
        <Button
          variant="outline"
          className="mt-4 w-full"
          onClick={() => navigate("/upload")}
        >
          <Plus className="mr-2 h-4 w-4" />
          Add Knowledge
        </Button>
      </div>
    </Card>
  );
};

export default KnowledgeBase;
