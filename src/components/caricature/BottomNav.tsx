'use client';

import { Home, History, Wand2, Settings, Moon, Sun } from 'lucide-react';
import { cn } from '@/lib/utils';

interface BottomNavProps {
  activeTab: 'create' | 'history';
  onTabChange: (tab: 'create' | 'history') => void;
  isDarkMode: boolean;
  onToggleDarkMode: () => void;
}

export function BottomNav({ activeTab, onTabChange, isDarkMode, onToggleDarkMode }: BottomNavProps) {
  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-background/95 backdrop-blur-lg border-t border-border safe-area-bottom">
      <div className="flex justify-around items-center h-16 max-w-lg mx-auto px-4">
        <button
          onClick={() => onTabChange('create')}
          className={cn(
            'flex flex-col items-center gap-1 py-2 px-4 rounded-xl transition-colors',
            activeTab === 'create'
              ? 'text-primary'
              : 'text-muted-foreground hover:text-foreground'
          )}
        >
          <Wand2 className="w-5 h-5" />
          <span className="text-xs font-medium">Create</span>
        </button>

        <button
          onClick={() => onTabChange('history')}
          className={cn(
            'flex flex-col items-center gap-1 py-2 px-4 rounded-xl transition-colors',
            activeTab === 'history'
              ? 'text-primary'
              : 'text-muted-foreground hover:text-foreground'
          )}
        >
          <History className="w-5 h-5" />
          <span className="text-xs font-medium">History</span>
        </button>

        <button
          onClick={onToggleDarkMode}
          className="flex flex-col items-center gap-1 py-2 px-4 rounded-xl text-muted-foreground hover:text-foreground transition-colors"
        >
          {isDarkMode ? (
            <>
              <Sun className="w-5 h-5" />
              <span className="text-xs font-medium">Light</span>
            </>
          ) : (
            <>
              <Moon className="w-5 h-5" />
              <span className="text-xs font-medium">Dark</span>
            </>
          )}
        </button>
      </div>
    </nav>
  );
}
