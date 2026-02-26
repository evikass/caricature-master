'use client';

import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { 
  Code, 
  Copy, 
  Download, 
  Check, 
  FileCode, 
  FileArchive,
  Info,
  Terminal
} from 'lucide-react';

interface CodeOutputProps {
  code: string;
  fileName: string;
  onDownload: () => void;
}

export default function CodeOutput({ code, fileName, onDownload }: CodeOutputProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      console.error('Failed to copy');
    }
  };

  // Parse the code to extract key information
  const codeStats = {
    lines: code.split('\n').length,
    totalParts: (code.match(/\.name = /g) || []).length,
    ballJoints: (code.match(/_ball/g) || []).length,
    bones: (code.match(/_bone/g) || []).length,
  };

  // Get code preview (first 50 lines)
  const codePreview = code.split('\n').slice(0, 50).join('\n');

  // Syntax highlighting simulation
  const highlightLine = (line: string) => {
    // Comments
    if (line.trim().startsWith('#')) {
      return <span className="text-emerald-400">{line}</span>;
    }
    // Strings
    if (line.includes('"') || line.includes("'")) {
      return <span>{line.replace(/(["'])(.*?)\1/g, '<span class="text-amber-400">$1$2$1</span>')}</span>;
    }
    // Keywords
    const keywords = ['import', 'from', 'def', 'return', 'if', 'else', 'for', 'in', 'class'];
    let highlighted = line;
    keywords.forEach(kw => {
      const regex = new RegExp(`\\b${kw}\\b`, 'g');
      highlighted = highlighted.replace(regex, `<span class="text-purple-400">${kw}</span>`);
    });
    // Numbers
    highlighted = highlighted.replace(/\b(\d+\.?\d*)\b/g, '<span class="text-cyan-400">$1</span>');
    
    return <span dangerouslySetInnerHTML={{ __html: highlighted }} />;
  };

  return (
    <Card className="border-slate-700 bg-slate-800/50 backdrop-blur h-full">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="text-lg flex items-center gap-2 text-white">
              <Code className="w-5 h-5 text-emerald-400" />
              Python скрипт для Blender
            </CardTitle>
            <CardDescription className="text-slate-400 mt-1">
              {fileName}
            </CardDescription>
          </div>
          <div className="flex gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={handleCopy}
              className="border-slate-600 text-slate-300 hover:bg-slate-700"
            >
              {copied ? (
                <>
                  <Check className="w-4 h-4 mr-1 text-emerald-400" />
                  Скопировано
                </>
              ) : (
                <>
                  <Copy className="w-4 h-4 mr-1" />
                  Копировать
                </>
              )}
            </Button>
            <Button
              size="sm"
              onClick={onDownload}
              className="bg-emerald-600 hover:bg-emerald-500 text-white"
            >
              <Download className="w-4 h-4 mr-1" />
              Скачать .py
            </Button>
          </div>
        </div>
      </CardHeader>
      <CardContent className="p-0">
        <Tabs defaultValue="preview" className="w-full">
          <TabsList className="w-full bg-slate-900/50 border-b border-slate-700 rounded-none h-auto p-0">
            <TabsTrigger 
              value="preview" 
              className="flex-1 data-[state=active]:bg-slate-800 data-[state=active]:border-b-2 data-[state=active]:border-emerald-500 rounded-none py-3"
            >
              <FileCode className="w-4 h-4 mr-2" />
              Превью кода
            </TabsTrigger>
            <TabsTrigger 
              value="info" 
              className="flex-1 data-[state=active]:bg-slate-800 data-[state=active]:border-b-2 data-[state=active]:border-emerald-500 rounded-none py-3"
            >
              <Info className="w-4 h-4 mr-2" />
              Инструкция
            </TabsTrigger>
          </TabsList>

          <TabsContent value="preview" className="m-0">
            {/* Stats bar */}
            <div className="flex items-center gap-4 px-4 py-2 bg-slate-900/80 border-b border-slate-700 text-xs text-slate-400">
              <span className="flex items-center gap-1">
                <Terminal className="w-3 h-3" />
                {codeStats.lines} строк
              </span>
              <Badge variant="outline" className="text-xs bg-slate-800 border-slate-600">
                {codeStats.totalParts} частей
              </Badge>
              <Badge variant="outline" className="text-xs bg-red-900/50 border-red-700 text-red-300">
                {codeStats.ballJoints} шарниров
              </Badge>
              <Badge variant="outline" className="text-xs bg-slate-800 border-slate-600">
                {codeStats.bones} костей
              </Badge>
            </div>

            {/* Code display */}
            <ScrollArea className="h-80">
              <pre className="p-4 text-xs font-mono text-slate-300 bg-slate-900">
                {codePreview.split('\n').map((line, i) => (
                  <div key={i} className="table-row">
                    <span className="table-cell pr-4 text-slate-600 select-none text-right w-12">
                      {i + 1}
                    </span>
                    <span className="table-cell">
                      {highlightLine(line)}
                    </span>
                  </div>
                ))}
                {code.split('\n').length > 50 && (
                  <div className="text-slate-500 text-center py-2 border-t border-slate-700">
                    ... и ещё {code.split('\n').length - 50} строк
                  </div>
                )}
              </pre>
            </ScrollArea>
          </TabsContent>

          <TabsContent value="info" className="m-0 p-4">
            <ScrollArea className="h-80">
              <div className="space-y-4 text-sm text-slate-300">
                <div className="p-4 bg-slate-900/80 rounded-lg border border-slate-700">
                  <h4 className="font-semibold text-white mb-2 flex items-center gap-2">
                    <Terminal className="w-4 h-4 text-emerald-400" />
                    Как использовать скрипт в Blender:
                  </h4>
                  <ol className="list-decimal list-inside space-y-2 text-slate-400">
                    <li>Откройте Blender (версия 3.0 или выше)</li>
                    <li>Перейдите во вкладку <code className="bg-slate-800 px-1 rounded">Scripting</code></li>
                    <li>Нажмите <code className="bg-slate-800 px-1 rounded">Open</code> и выберите скачанный .py файл</li>
                    <li>Нажмите кнопку <code className="bg-slate-800 px-1 rounded">Run Script</code> (или Shift+Alt+P)</li>
                    <li>Готово! Каркас появится во вьюпорте</li>
                  </ol>
                </div>

                <div className="p-4 bg-slate-900/80 rounded-lg border border-slate-700">
                  <h4 className="font-semibold text-white mb-2 flex items-center gap-2">
                    <FileArchive className="w-4 h-4 text-amber-400" />
                    Экспорт для 3D печати:
                  </h4>
                  <ol className="list-decimal list-inside space-y-2 text-slate-400">
                    <li>Выделите нужные части каркаса</li>
                    <li>Файл → Экспорт → STL (.stl)</li>
                    <li>Импортируйте в слайсер для SLA печати</li>
                    <li>Настройте ориентацию для оптимальной печати</li>
                  </ol>
                </div>

                <div className="p-4 bg-amber-900/20 rounded-lg border border-amber-700/50">
                  <h4 className="font-semibold text-amber-400 mb-2">Важные настройки для SLA:</h4>
                  <ul className="list-disc list-inside space-y-1 text-amber-200/70 text-xs">
                    <li>Высота слоя: 0.05 мм для лучших деталей</li>
                    <li>Экспозиция: следуйте рекомендациям производителя смолы</li>
                    <li>Ориентация: шары печатайте опорной точкой вверх</li>
                    <li>Сокеты: печатайте открытием вверх</li>
                  </ul>
                </div>

                <div className="p-4 bg-emerald-900/20 rounded-lg border border-emerald-700/50">
                  <h4 className="font-semibold text-emerald-400 mb-2">Сборка после печати:</h4>
                  <ul className="list-disc list-inside space-y-1 text-emerald-200/70 text-xs">
                    <li>Тщательно очистите все части после печати</li>
                    <li>Проверьте подгонку всех шарниров перед финальной сборкой</li>
                    <li>Используйте эпоксидный клей для постоянных соединений</li>
                    <li>Отшлифуйте контактные поверхности для лучшей посадки</li>
                  </ul>
                </div>
              </div>
            </ScrollArea>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  );
}
