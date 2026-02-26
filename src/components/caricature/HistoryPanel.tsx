'use client';

import { History, Trash2, Download, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { CaricatureHistoryItem } from '@/types/caricature';
import { STYLE_OPTIONS } from './config';

interface HistoryPanelProps {
  history: CaricatureHistoryItem[];
  onSelect: (item: CaricatureHistoryItem) => void;
  onClear: () => void;
  onDelete: (id: string) => void;
  isOpen: boolean;
  onClose: () => void;
}

export function HistoryPanel({
  history,
  onSelect,
  onClear,
  onDelete,
  isOpen,
  onClose,
}: HistoryPanelProps) {
  if (!isOpen) return null;

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const hours = Math.floor(diff / (1000 * 60 * 60));
    
    if (hours < 1) return 'Just now';
    if (hours < 24) return `${hours}h ago`;
    return date.toLocaleDateString();
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-end justify-center">
      <div className="w-full max-w-lg bg-background rounded-t-3xl max-h-[80vh] flex flex-col animate-in slide-in-from-bottom duration-300">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b">
          <div className="flex items-center gap-2">
            <History className="w-5 h-5 text-muted-foreground" />
            <h2 className="text-lg font-semibold">History</h2>
            <span className="text-xs text-muted-foreground bg-muted px-2 py-1 rounded-full">
              {history.length} items
            </span>
          </div>
          <div className="flex items-center gap-2">
            {history.length > 0 && (
              <Button
                variant="ghost"
                size="sm"
                className="text-destructive hover:text-destructive"
                onClick={onClear}
              >
                <Trash2 className="w-4 h-4 mr-1" />
                Clear
              </Button>
            )}
            <Button variant="ghost" size="icon" onClick={onClose}>
              <X className="w-5 h-5" />
            </Button>
          </div>
        </div>

        {/* Content */}
        <ScrollArea className="flex-1 p-4">
          {history.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <div className="w-16 h-16 rounded-full bg-muted flex items-center justify-center mb-4">
                <History className="w-8 h-8 text-muted-foreground" />
              </div>
              <p className="text-muted-foreground">No caricatures yet</p>
              <p className="text-sm text-muted-foreground/70 mt-1">
                Your creations will appear here
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-2 gap-3">
              {history.map((item) => {
                const style = STYLE_OPTIONS.find((s) => s.id === item.style);
                return (
                  <button
                    key={item.id}
                    className="relative group rounded-xl overflow-hidden shadow-sm hover:shadow-md transition-shadow"
                    onClick={() => onSelect(item)}
                  >
                    <img
                      src={item.caricatureImage}
                      alt="Caricature"
                      className="w-full aspect-square object-cover"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity">
                      <div className="absolute bottom-0 left-0 right-0 p-2 flex items-center justify-between">
                        <div>
                          <span className="text-xs text-white/80 flex items-center gap-1">
                            <span>{style?.emoji}</span>
                            <span>{style?.name}</span>
                          </span>
                          <p className="text-xs text-white/60">
                            {formatDate(item.createdAt)}
                          </p>
                        </div>
                        <button
                          className="p-1.5 bg-white/20 backdrop-blur-sm rounded-full hover:bg-white/30 transition-colors"
                          onClick={(e) => {
                            e.stopPropagation();
                            onDelete(item.id);
                          }}
                        >
                          <Trash2 className="w-3 h-3 text-white" />
                        </button>
                      </div>
                    </div>
                  </button>
                );
              })}
            </div>
          )}
        </ScrollArea>
      </div>
    </div>
  );
}
