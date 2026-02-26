'use client';

import { useState, useCallback, Suspense } from 'react';
import dynamic from 'next/dynamic';
import { Skeleton } from '@/components/ui/skeleton';
import { Badge } from '@/components/ui/badge';
import { 
  Bot, 
  Sparkles, 
  Settings2, 
  Code2, 
  Eye,
  Loader2,
  AlertCircle,
  Download
} from 'lucide-react';
import type { ArmatureConfig } from '@/lib/armatureScript';
import { defaultConfig, generateBlenderArmatureScript } from '@/lib/armatureScript';
import ConfigPanel from '@/components/ConfigPanel';

// Dynamic import for 3D component (no SSR)
const ArmatureViewer = dynamic(
  () => import('@/components/ArmatureViewer'),
  { 
    ssr: false,
    loading: () => (
      <div className="w-full h-full flex items-center justify-center bg-slate-900 rounded-lg">
        <div className="text-center">
          <Loader2 className="w-12 h-12 text-emerald-400 animate-spin mx-auto mb-4" />
          <p className="text-slate-400">Загрузка 3D превью...</p>
        </div>
      </div>
    ),
  }
);

export default function Home() {
  const [config, setConfig] = useState<ArmatureConfig>(defaultConfig);
  const [isGenerating, setIsGenerating] = useState(false);

  const handleConfigChange = useCallback((newConfig: Partial<ArmatureConfig>) => {
    setConfig(prev => ({ ...prev, ...newConfig }));
  }, []);

  const handleGenerate = useCallback(() => {
    setIsGenerating(true);
    try {
      const script = generateBlenderArmatureScript(config);
      
      // Create blob and download
      const blob = new Blob([script], { type: 'text/plain' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'blender_puppet_armature.py';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Generation failed:', error);
    } finally {
      setIsGenerating(false);
    }
  }, [config]);

  const handleReset = useCallback(() => {
    setConfig(defaultConfig);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur-lg sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center shadow-lg shadow-emerald-500/25">
                <Bot className="w-7 h-7 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-white flex items-center gap-2">
                  Каркасы для кукольной анимации
                  <Badge variant="outline" className="text-xs bg-emerald-600/20 border-emerald-500/50 text-emerald-400">
                    v2.0
                  </Badge>
                </h1>
                <p className="text-sm text-slate-400">
                  Генератор каркасов для Blender
                </p>
              </div>
            </div>
            <div className="hidden md:flex items-center gap-6 text-sm text-slate-400">
              <span className="flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-amber-400" />
                3 типа каркасов
              </span>
              <span className="flex items-center gap-2">
                <Settings2 className="w-4 h-4 text-blue-400" />
                SLA-оптимизация
              </span>
              <span className="flex items-center gap-2">
                <Code2 className="w-4 h-4 text-purple-400" />
                Blender 3.0+
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">
            Создавайте <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-teal-400">профессиональные каркасы</span>
          </h2>
          <p className="text-lg text-slate-400 max-w-2xl mx-auto">
            Генератор Python-скриптов для Blender для создания 3D-печатных каркасов 
            кукольной анимации с шарнирами ball-and-socket
          </p>
        </div>
      </section>

      {/* Main Content */}
      <main className="container mx-auto px-4 pb-6">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Left Panel - Configuration */}
          <div className="lg:col-span-4 space-y-4">
            <ConfigPanel
              config={config}
              onConfigChange={handleConfigChange}
              onGenerate={handleGenerate}
              onReset={handleReset}
              isGenerating={isGenerating}
            />
          </div>

          {/* Right Panel - 3D Viewer */}
          <div className="lg:col-span-8 space-y-4">
            {/* 3D Preview */}
            <div className="rounded-xl border border-slate-700 overflow-hidden shadow-xl shadow-slate-900/50">
              <div className="bg-slate-800/50 px-4 py-2 border-b border-slate-700 flex items-center justify-between">
                <div className="flex items-center gap-2 text-sm text-slate-400">
                  <div className="flex gap-1.5">
                    <div className="w-3 h-3 rounded-full bg-red-500"></div>
                    <div className="w-3 h-3 rounded-full bg-amber-500"></div>
                    <div className="w-3 h-3 rounded-full bg-emerald-500"></div>
                  </div>
                  <span className="ml-2">Интерактивное 3D превью</span>
                </div>
                <div className="flex items-center gap-4 text-xs text-slate-500">
                  <span>Тип: {
                    config.armatureType === 'humanoid' ? 'Гуманоид' : 
                    config.armatureType === 'simple' ? 'Простой' : 'Животное'
                  }</span>
                  <span>Масштаб: {config.scaleFactor.toFixed(1)}x</span>
                </div>
              </div>
              <div className="h-[500px] relative">
                <Suspense fallback={
                  <div className="w-full h-full flex items-center justify-center bg-slate-900">
                    <div className="text-center">
                      <Loader2 className="w-12 h-12 text-emerald-400 animate-spin mx-auto mb-4" />
                      <p className="text-slate-400">Загрузка 3D превью...</p>
                    </div>
                  </div>
                }>
                  <ArmatureViewer config={config} />
                </Suspense>
                
                {/* Preview Controls Hint */}
                <div className="absolute bottom-4 left-4 right-4 flex justify-center">
                  <div className="bg-slate-900/90 backdrop-blur-sm px-4 py-2 rounded-lg border border-slate-700 text-xs text-slate-400 flex items-center gap-4">
                    <span className="flex items-center gap-1">
                      <kbd className="px-1.5 py-0.5 bg-slate-800 rounded text-slate-300">ЛКМ</kbd>
                      Вращение
                    </span>
                    <span className="flex items-center gap-1">
                      <kbd className="px-1.5 py-0.5 bg-slate-800 rounded text-slate-300">Колёсико</kbd>
                      Масштаб
                    </span>
                    <span className="flex items-center gap-1">
                      <kbd className="px-1.5 py-0.5 bg-slate-800 rounded text-slate-300">ПКМ</kbd>
                      Перемещение
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Legend */}
            <div className="rounded-xl border border-slate-700 bg-slate-800/30 p-4">
              <h3 className="text-sm font-medium text-white mb-3 flex items-center gap-2">
                <Eye className="w-4 h-4 text-emerald-400" />
                Легенда цветов
              </h3>
              <div className="flex flex-wrap gap-4">
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 rounded-full bg-red-500"></div>
                  <span className="text-sm text-slate-400">Шарниры (ball joints)</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 rounded bg-blue-500"></div>
                  <span className="text-sm text-slate-400">Кости (bones)</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 rounded bg-gray-500"></div>
                  <span className="text-sm text-slate-400">Части тела (body parts)</span>
                </div>
              </div>
            </div>

            {/* Quick Stats */}
            <div className="grid grid-cols-4 gap-3">
              <div className="p-4 bg-slate-800/50 border border-slate-700 rounded-lg text-center">
                <div className="text-2xl font-bold text-emerald-400">{config.scaleFactor.toFixed(1)}x</div>
                <div className="text-xs text-slate-400">масштаб</div>
              </div>
              <div className="p-4 bg-slate-800/50 border border-slate-700 rounded-lg text-center">
                <div className="text-2xl font-bold text-red-400">{config.ballJointRadius.toFixed(1)}</div>
                <div className="text-xs text-slate-400">мм шарнир</div>
              </div>
              <div className="p-4 bg-slate-800/50 border border-slate-700 rounded-lg text-center">
                <div className="text-2xl font-bold text-blue-400">{config.socketGap.toFixed(2)}</div>
                <div className="text-xs text-slate-400">мм зазор</div>
              </div>
              <div className="p-4 bg-slate-800/50 border border-slate-700 rounded-lg text-center">
                <div className="text-2xl font-bold text-purple-400">{config.boneDiameter.toFixed(1)}</div>
                <div className="text-xs text-slate-400">мм кость</div>
              </div>
            </div>

            {/* Download Button for Mobile */}
            <div className="lg:hidden">
              <button
                onClick={handleGenerate}
                disabled={isGenerating}
                className="w-full bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-semibold py-4 rounded-lg shadow-lg shadow-emerald-500/25 transition-all duration-200 flex items-center justify-center gap-2"
              >
                <Download className="w-5 h-5" />
                {isGenerating ? 'Генерация...' : 'Скачать скрипт Blender'}
              </button>
            </div>
          </div>
        </div>

        {/* Features Section */}
        <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="p-6 bg-gradient-to-br from-slate-800/50 to-slate-900/50 border border-slate-700 rounded-xl">
            <div className="w-12 h-12 rounded-lg bg-emerald-600/20 flex items-center justify-center mb-4">
              <Settings2 className="w-6 h-6 text-emerald-400" />
            </div>
            <h3 className="text-lg font-semibold text-white mb-2">SLA-оптимизация</h3>
            <p className="text-sm text-slate-400">
              Все модели оптимизированы для SLA 3D-печати с правильными зазорами, 
              минимальной толщиной стенок и плоскими основаниями.
            </p>
          </div>

          <div className="p-6 bg-gradient-to-br from-slate-800/50 to-slate-900/50 border border-slate-700 rounded-xl">
            <div className="w-12 h-12 rounded-lg bg-red-600/20 flex items-center justify-center mb-4">
              <Bot className="w-6 h-6 text-red-400" />
            </div>
            <h3 className="text-lg font-semibold text-white mb-2">Ball-and-Socket шарниры</h3>
            <p className="text-sm text-slate-400">
              Профессиональные сферические шарниры с точными допусками 
              для плавной анимации и надёжной фиксации поз.
            </p>
          </div>

          <div className="p-6 bg-gradient-to-br from-slate-800/50 to-slate-900/50 border border-slate-700 rounded-xl">
            <div className="w-12 h-12 rounded-lg bg-purple-600/20 flex items-center justify-center mb-4">
              <Code2 className="w-6 h-6 text-purple-400" />
            </div>
            <h3 className="text-lg font-semibold text-white mb-2">Blender интеграция</h3>
            <p className="text-sm text-slate-400">
              Генерация готовых Python скриптов для Blender с возможностью 
              дальнейшей настройки и модификации.
            </p>
          </div>
        </div>

        {/* Info Alert */}
        <div className="mt-8 p-4 bg-amber-900/20 border border-amber-700/50 rounded-xl flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-amber-400 mt-0.5 flex-shrink-0" />
          <div className="text-sm text-amber-200/80">
            <strong className="text-amber-400">Совет:</strong> Для лучших результатов используйте Blender 3.0 или выше. 
            Сгенерированный скрипт создаёт полностью параметрический каркас, который можно модифицировать 
            прямо в Blender перед экспортом в STL для 3D-печати.
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800 mt-12 py-6 bg-slate-900/50">
        <div className="container mx-auto px-4 text-center text-sm text-slate-500">
          <p>Puppet Armature Generator • Каркасы для кукольной анимации</p>
        </div>
      </footer>
    </div>
  );
}
