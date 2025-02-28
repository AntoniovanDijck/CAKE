import React, { useState } from "react";
import { Upload, FileUp } from "lucide-react";
import { cn } from "@/lib/utils";
import { Card } from "@/components/ui/card";

interface UploadZoneProps {
  onFileSelect?: (file: File) => void;
  isUploading?: boolean;
  acceptedFileTypes?: string[];
}

const UploadZone = ({
  onFileSelect = () => {},
  isUploading = false,
  acceptedFileTypes = [
    ".mp4",
    ".mov",
    ".avi",
    ".mp3",
    ".wav",
    ".m4a",
    ".txt",
    ".doc",
    ".docx",
    ".pdf",
  ],
}: UploadZoneProps) => {
  const [isDragging, setIsDragging] = useState(false);

  const handleDragEnter = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      onFileSelect(files[0]);
    }
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      onFileSelect(files[0]);
    }
  };

  return (
    <Card
      className="bg-background w-full max-w-[800px] aspect-[2/1] mx-auto rounded-lg border-2 border-dashed relative transition-all duration-300 ease-in-out hover:border-primary"
      style={{
        borderColor: isDragging ? "hsl(var(--primary))" : "hsl(var(--border))",
      }}
    >
      <input
        type="file"
        className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
        onChange={handleFileInput}
        accept={acceptedFileTypes.join(",")}
        disabled={isUploading}
      />
      <div
        className={cn(
          "absolute inset-0 flex flex-col items-center justify-center p-6",
          isDragging && "bg-muted/50",
        )}
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
      >
        <div className="mb-4 rounded-full p-4 bg-muted">
          {isUploading ? (
            <Upload className="w-12 h-12 text-muted-foreground animate-pulse" />
          ) : (
            <FileUp className="w-12 h-12 text-muted-foreground" />
          )}
        </div>
        <h3 className="text-lg font-semibold mb-2">
          {isUploading ? "Uploading..." : "Drag & Drop your video here"}
        </h3>
        <p className="text-sm text-muted-foreground mb-4 text-center">
          {isUploading
            ? "Please wait while we process your file"
            : `or click to select a file from your computer
${acceptedFileTypes.join(", ")} accepted`}
        </p>
      </div>
    </Card>
  );
};

export default UploadZone;
