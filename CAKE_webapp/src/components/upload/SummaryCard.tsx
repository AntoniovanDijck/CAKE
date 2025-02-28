import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Clock, FileText, Tag, User, X, Plus } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useState, useEffect } from "react";

interface ExtractedInfo {
  title: string;
  duration: string;
  tags: string[];
  transcript: string;
  speaker: string;
  knowledgeGraph: Array<{
    subject: string;
    predicate: string;
    object: string;
  }>;
}

interface SummaryCardProps {
  extractedInfo?: ExtractedInfo;
  isVisible?: boolean;
  onUpdate?: (info: ExtractedInfo) => void;
}

const defaultInfo: ExtractedInfo = {
  title: "My First Vlog",
  duration: "5:32",
  tags: ["travel", "adventure", "daily life"],
  transcript:
    "Hey everyone! Welcome to my first vlog. Today we're going to explore the beautiful city of Paris. The architecture here is amazing, especially the Eiffel Tower. I've been learning about the history of this place and it's fascinating how it was built...",
  speaker: "John Doe",
  knowledgeGraph: [
    { subject: "Eiffel Tower", predicate: "location", object: "Paris" },
    { subject: "Paris", predicate: "has", object: "beautiful architecture" },
    { subject: "speaker", predicate: "is exploring", object: "Paris" },
    { subject: "Eiffel Tower", predicate: "is", object: "amazing" },
  ],
};

const SummaryCard = ({
  extractedInfo = defaultInfo,
  isVisible = true,
  onUpdate,
}: SummaryCardProps) => {
  const [title, setTitle] = useState(extractedInfo.title);
  const [speaker, setSpeaker] = useState(extractedInfo.speaker);
  const [newTag, setNewTag] = useState("");
  const [tags, setTags] = useState(extractedInfo.tags);

  useEffect(() => {
    setTitle(extractedInfo.title);
    setSpeaker(extractedInfo.speaker);
    setTags(extractedInfo.tags);
  }, [extractedInfo]);

  const handleAddTag = () => {
    if (newTag.trim() && !tags.includes(newTag.trim())) {
      const updatedTags = [...tags, newTag.trim()];
      setTags(updatedTags);
      setNewTag("");
      onUpdate?.({ ...extractedInfo, tags: updatedTags });
    }
  };

  const handleRemoveTag = (tagToRemove: string) => {
    const updatedTags = tags.filter((tag) => tag !== tagToRemove);
    setTags(updatedTags);
    onUpdate?.({ ...extractedInfo, tags: updatedTags });
  };

  const handleTitleChange = (newTitle: string) => {
    setTitle(newTitle);
    onUpdate?.({ ...extractedInfo, title: newTitle });
  };

  const handleSpeakerChange = (newSpeaker: string) => {
    setSpeaker(newSpeaker);
    onUpdate?.({ ...extractedInfo, speaker: newSpeaker });
  };
  return (
    <div
      className={`fixed bottom-0 left-0 right-0 bg-background/80 backdrop-blur-sm transition-all duration-300 transform ${isVisible ? "translate-y-0" : "translate-y-full"}`}
    >
      <Card className="mx-auto max-w-3xl mb-4 shadow-lg border-2">
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <span>Processing Summary</span>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 gap-4">
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <FileText className="w-5 h-5 text-primary" />
                <span className="font-medium">Title:</span>
                <Input
                  value={title}
                  onChange={(e) => handleTitleChange(e.target.value)}
                  className="flex-1 h-8"
                  placeholder="Enter title..."
                />
              </div>

              <div className="flex items-center gap-2">
                <Clock className="w-5 h-5 text-primary" />
                <span className="font-medium">Duration:</span>
                <span>{extractedInfo.duration}</span>
              </div>

              <div className="flex items-center gap-2">
                <User className="w-5 h-5 text-primary" />
                <span className="font-medium">Speaker:</span>
                <Input
                  value={speaker}
                  onChange={(e) => handleSpeakerChange(e.target.value)}
                  className="flex-1 h-8"
                  placeholder="Enter speaker name..."
                />
              </div>

              <div className="flex items-center gap-2 flex-wrap">
                <Tag className="w-5 h-5 text-primary" />
                <span className="font-medium">Tags:</span>
                <div className="flex-1 flex flex-wrap gap-2">
                  {tags.map((tag, index) => (
                    <Badge
                      key={index}
                      variant="secondary"
                      className="flex items-center gap-1"
                    >
                      {tag}
                      <button
                        onClick={() => handleRemoveTag(tag)}
                        className="hover:text-destructive"
                      >
                        <X className="h-3 w-3" />
                      </button>
                    </Badge>
                  ))}
                  <div className="flex gap-2">
                    <Input
                      value={newTag}
                      onChange={(e) => setNewTag(e.target.value)}
                      className="h-8 w-32"
                      placeholder="New tag..."
                      onKeyPress={(e) => e.key === "Enter" && handleAddTag()}
                    />
                    <Button
                      size="sm"
                      variant="outline"
                      className="h-8"
                      onClick={handleAddTag}
                    >
                      <Plus className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </div>
            </div>

            <div className="space-y-4 mt-4">
              <div className="space-y-2">
                <span className="font-medium">Transcript:</span>
                <ScrollArea className="h-[100px] w-full rounded-md border p-4">
                  <p className="text-sm">{extractedInfo.transcript}</p>
                </ScrollArea>
              </div>

              <div className="space-y-2">
                <span className="font-medium">Extracted Knowledge:</span>
                <ScrollArea className="h-[200px] w-full rounded-md border p-4">
                  <div className="space-y-2">
                    {extractedInfo.knowledgeGraph.map((item, index) => (
                      <div key={index} className="p-2 bg-muted rounded-md">
                        <div className="flex items-center gap-2 text-sm">
                          <span className="font-medium">{item.subject}</span>
                          <span className="text-muted-foreground">
                            {item.predicate}
                          </span>
                          <span className="font-medium">{item.object}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </ScrollArea>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default SummaryCard;
