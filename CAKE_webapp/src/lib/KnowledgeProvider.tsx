import React, { createContext, useContext, useState } from "react";

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
  enabled?: boolean;
}

type KnowledgeContextType = {
  knowledgeBases: KnowledgeBase[];
  setKnowledgeBases: React.Dispatch<React.SetStateAction<KnowledgeBase[]>>;
};

const KnowledgeContext = createContext<KnowledgeContextType | undefined>(
  undefined,
);

export function KnowledgeProvider({ children }: { children: React.ReactNode }) {
  const [knowledgeBases, setKnowledgeBases] = useState<KnowledgeBase[]>([]);

  return (
    <KnowledgeContext.Provider value={{ knowledgeBases, setKnowledgeBases }}>
      {children}
    </KnowledgeContext.Provider>
  );
}

export function useKnowledge() {
  const context = useContext(KnowledgeContext);
  if (context === undefined) {
    throw new Error("useKnowledge must be used within a KnowledgeProvider");
  }
  return context;
}
