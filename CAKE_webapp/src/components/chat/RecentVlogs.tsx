import React from "react";
import { Card } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Video } from "lucide-react";

interface Vlog {
  id: string;
  title: string;
  duration: string;
  timestamp: Date;
}

const RecentVlogs = () => {
  const vlogs: Vlog[] = [
    {
      id: "1",
      title: "My First Vlog",
      duration: "5:32",
      timestamp: new Date(),
    },
    {
      id: "2",
      title: "Travel Adventures",
      duration: "10:15",
      timestamp: new Date(),
    },
    {
      id: "3",
      title: "Daily Life",
      duration: "7:45",
      timestamp: new Date(),
    },
  ];

  return (
    <Card className="p-4 h-full bg-background">
      <h3 className="font-semibold mb-4">Recent Vlogs</h3>
      <ScrollArea className="h-[calc(100%-2rem)]">
        <div className="space-y-2">
          {vlogs.map((vlog) => (
            <div
              key={vlog.id}
              className="flex items-center gap-3 p-2 rounded-lg hover:bg-muted cursor-pointer"
            >
              <Video className="h-4 w-4 text-muted-foreground" />
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium truncate">{vlog.title}</p>
                <div className="flex items-center gap-2 text-xs text-muted-foreground">
                  <span>{vlog.duration}</span>
                  <span>•</span>
                  <span>{vlog.timestamp.toLocaleDateString()}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </ScrollArea>
    </Card>
  );
};

export default RecentVlogs;
