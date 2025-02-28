import React, { useState } from "react";
import UploadZone from "@/components/upload/UploadZone";
import ProgressIndicator from "@/components/upload/ProgressIndicator";
import SummaryCard from "@/components/upload/SummaryCard";
import { motion } from "framer-motion";
import { fadeIn, slideUp, pageTransition } from "@/lib/animations";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
  FileVideo,
  FileAudio,
  FileText,
  Plus,
  Video,
  AudioLines,
  File,
  ArrowLeft,
} from "lucide-react";
import { ScrollArea } from "@/components/ui/scroll-area";

type DataType = "video" | "audio" | "text" | null;

interface UploadedContent {
  id: string;
  type: DataType;
  name: string;
  date: Date;
  status: "processing" | "complete";
  extractedInfo?: {
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
  };
}

const UploadPage = () => {
  const [isUploading, setIsUploading] = useState(false);
  const [selectedType, setSelectedType] = useState<DataType>(null);
  const [uploadStatus, setUploadStatus] = useState<
    "idle" | "uploading" | "processing" | "complete"
  >("idle");
  const [progress, setProgress] = useState(0);
  const [showSummary, setShowSummary] = useState(false);
  const [selectedContent, setSelectedContent] =
    useState<UploadedContent | null>(null);
  const [uploadedContent, setUploadedContent] = useState<UploadedContent[]>([
    {
      id: "1",
      type: "video",
      name: "Travel Vlog - Paris.mp4",
      date: new Date(),
      status: "complete",
      extractedInfo: {
        title: "Travel Vlog - Paris",
        duration: "5:32",
        tags: ["travel", "paris", "architecture"],
        transcript:
          "Hey everyone! Welcome to my Paris vlog. Today we're exploring the beautiful city of Paris. The architecture here is amazing, especially the Eiffel Tower...",
        speaker: "Sarah Smith",
        knowledgeGraph: [
          { subject: "Eiffel Tower", predicate: "location", object: "Paris" },
          {
            subject: "Paris",
            predicate: "has",
            object: "beautiful architecture",
          },
          { subject: "Sarah", predicate: "is exploring", object: "Paris" },
        ],
      },
    },
    {
      id: "2",
      type: "audio",
      name: "History Podcast.mp3",
      date: new Date(),
      status: "complete",
      extractedInfo: {
        title: "History of Architecture",
        duration: "15:45",
        tags: ["history", "architecture", "podcast"],
        transcript:
          "In today's episode, we'll be discussing the evolution of architectural styles throughout history...",
        speaker: "Prof. Johnson",
        knowledgeGraph: [
          {
            subject: "Gothic Architecture",
            predicate: "period",
            object: "Medieval Era",
          },
          {
            subject: "Renaissance",
            predicate: "influenced",
            object: "Modern Architecture",
          },
        ],
      },
    },
    {
      id: "3",
      type: "text",
      name: "Research Notes.pdf",
      date: new Date(),
      status: "complete",
      extractedInfo: {
        title: "Architecture Research Notes",
        duration: "N/A",
        tags: ["research", "notes", "architecture"],
        transcript:
          "These notes cover the fundamental principles of architectural design and their historical context...",
        speaker: "N/A",
        knowledgeGraph: [
          {
            subject: "Architecture",
            predicate: "requires",
            object: "Design Principles",
          },
          {
            subject: "Design Principles",
            predicate: "include",
            object: "Balance",
          },
        ],
      },
    },
  ]);

  const handleFileSelect = (file: File) => {
    setUploadStatus("uploading");
    setProgress(0);
    setShowSummary(false);

    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          setUploadStatus("processing");
          setTimeout(() => {
            setUploadStatus("complete");
            setShowSummary(true);
            const newContent: UploadedContent = {
              id: Date.now().toString(),
              type: selectedType,
              name: file.name,
              date: new Date(),
              status: "complete",
              extractedInfo: {
                title: file.name.replace(/\.[^/.]+$/, ""),
                duration: selectedType === "text" ? "N/A" : "0:00",
                tags: [],
                transcript: "Processing transcript...",
                speaker: selectedType === "text" ? "N/A" : "Unknown",
                knowledgeGraph: [],
              },
            };
            setUploadedContent((prev) => [newContent, ...prev]);
            setSelectedContent(newContent);
            setIsUploading(false);
            setSelectedType(null);
          }, 2000);
          return 100;
        }
        return prev + 10;
      });
    }, 500);
  };

  const getAcceptedTypes = () => {
    switch (selectedType) {
      case "video":
        return [".mp4", ".mov", ".avi"];
      case "audio":
        return [".mp3", ".wav", ".m4a"];
      case "text":
        return [".txt", ".doc", ".docx", ".pdf"];
      default:
        return [];
    }
  };

  const getTypeIcon = (type: DataType) => {
    switch (type) {
      case "video":
        return <Video className="h-4 w-4" />;
      case "audio":
        return <AudioLines className="h-4 w-4" />;
      case "text":
        return <File className="h-4 w-4" />;
      default:
        return null;
    }
  };

  return (
    <motion.div
      className="h-screen p-6 flex flex-col"
      initial="initial"
      animate="animate"
      exit="exit"
      variants={fadeIn}
      transition={pageTransition}
    >
      <motion.div className="space-y-4 mb-6" variants={slideUp}>
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold">
            {isUploading ? "Upload New Content" : "Uploaded Content"}
          </h1>
          {!isUploading && (
            <Button onClick={() => setIsUploading(true)}>
              <Plus className="h-4 w-4 mr-2" />
              Upload New
            </Button>
          )}
        </div>
        {isUploading && (
          <Button variant="ghost" onClick={() => setIsUploading(false)}>
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back
          </Button>
        )}
      </motion.div>

      {isUploading ? (
        <motion.div
          className="flex-1 flex flex-col gap-6 min-h-0"
          variants={slideUp}
        >
          {!selectedType ? (
            <div className="flex-1 flex flex-col items-center justify-center">
              <Card className="p-8 w-full max-w-2xl mx-auto">
                <h2 className="text-xl font-semibold mb-6 text-center">
                  Select Content Type
                </h2>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  <Button
                    variant="outline"
                    className="h-32 flex flex-col gap-2"
                    onClick={() => setSelectedType("video")}
                  >
                    <FileVideo className="h-8 w-8" />
                    <span>Video</span>
                  </Button>
                  <Button
                    variant="outline"
                    className="h-32 flex flex-col gap-2"
                    onClick={() => setSelectedType("audio")}
                  >
                    <FileAudio className="h-8 w-8" />
                    <span>Audio</span>
                  </Button>
                  <Button
                    variant="outline"
                    className="h-32 flex flex-col gap-2"
                    onClick={() => setSelectedType("text")}
                  >
                    <FileText className="h-8 w-8" />
                    <span>Text</span>
                  </Button>
                </div>
              </Card>
            </div>
          ) : (
            <>
              <div className="flex-1 min-h-0 flex flex-col items-center justify-center">
                <UploadZone
                  onFileSelect={handleFileSelect}
                  isUploading={uploadStatus === "uploading"}
                  acceptedFileTypes={getAcceptedTypes()}
                />
              </div>
              {uploadStatus !== "idle" && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 20 }}
                >
                  <ProgressIndicator
                    status={uploadStatus}
                    progress={progress}
                  />
                </motion.div>
              )}
            </>
          )}
        </motion.div>
      ) : (
        <motion.div variants={slideUp} className="flex-1 min-h-0">
          <ScrollArea className="h-full">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 p-1">
              {uploadedContent.map((content) => (
                <Card
                  key={content.id}
                  className={`p-4 flex items-start gap-3 cursor-pointer transition-all hover:shadow-md hover:scale-[1.02] ${selectedContent?.id === content.id ? "ring-2 ring-primary" : ""}`}
                  onClick={() => setSelectedContent(content)}
                >
                  {getTypeIcon(content.type)}
                  <div className="flex-1 min-w-0">
                    <p className="font-medium truncate">{content.name}</p>
                    <div className="flex items-center gap-2 text-sm text-muted-foreground">
                      <span>{content.date.toLocaleDateString()}</span>
                      <span>•</span>
                      <span
                        className={
                          content.status === "processing"
                            ? "text-yellow-500"
                            : "text-green-500"
                        }
                      >
                        {content.status}
                      </span>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          </ScrollArea>
        </motion.div>
      )}
      {selectedContent && selectedContent.extractedInfo && (
        <SummaryCard
          extractedInfo={selectedContent.extractedInfo}
          isVisible={true}
          onUpdate={(updatedInfo) => {
            setUploadedContent((prev) =>
              prev.map((content) =>
                content.id === selectedContent.id
                  ? { ...content, extractedInfo: updatedInfo }
                  : content,
              ),
            );
            setSelectedContent((prev) =>
              prev ? { ...prev, extractedInfo: updatedInfo } : null,
            );
          }}
        />
      )}
    </motion.div>
  );
};

export default UploadPage;
