'use client';

import { useState, useRef, useCallback, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Camera, 
  ImagePlus, 
  Wand2, 
  Download, 
  Share2, 
  History, 
  Sparkles,
  ChevronLeft,
  ChevronRight,
  Loader2,
  Trash2,
  ZoomIn,
  ZoomOut,
  RotateCcw,
  X,
  Palette,
  Sliders,
  Home,
  User,
  Settings,
  Info
} from 'lucide-react';
import { cn } from '@/lib/utils';

// Types
interface CaricatureStyle {
  id: string;
  name: string;
  nameRu: string;
  icon: string;
  description: string;
}

interface HistoryItem {
  id: string;
  originalImage: string;
  caricatureImage: string;
  style: string;
  intensity: number;
  createdAt: number;
}

// Styles available
const CARICATURE_STYLES: CaricatureStyle[] = [
  { id: 'funny', name: 'Funny', nameRu: 'Смешной', icon: '😂', description: 'Комичный и забавный стиль' },
  { id: 'cartoon', name: 'Cartoon', nameRu: 'Мультяшный', icon: '🎨', description: 'Яркий мультяшный стиль' },
  { id: 'artistic', name: 'Artistic', nameRu: 'Художественный', icon: '🖼️', description: 'Художественная стилизация' },
  { id: 'comic', name: 'Comic', nameRu: 'Комикс', icon: '💥', description: 'Стиль комиксов' },
  { id: 'sketch', name: 'Sketch', nameRu: 'Скетч', icon: '✏️', description: 'Рисунок карандашом' },
  { id: 'anime', name: 'Anime', nameRu: 'Аниме', icon: '🌸', description: 'Стиль японской анимации' },
  { id: 'realistic', name: 'Realistic', nameRu: 'Реалистичный', icon: '🎭', description: 'Тонкая стилизация' },
];

export default function CaricatureApp() {
  // State
  const [activeTab, setActiveTab] = useState<'create' | 'history' | 'profile'>('create');
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [generatedImage, setGeneratedImage] = useState<string | null>(null);
  const [selectedStyle, setSelectedStyle] = useState<string>('funny');
  const [intensity, setIntensity] = useState<number>(50);
  const [isGenerating, setIsGenerating] = useState<boolean>(false);
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [zoom, setZoom] = useState<number>(1);
  const [showTutorial, setShowTutorial] = useState<boolean>(false);
  
  // Refs
  const fileInputRef = useRef<HTMLInputElement>(null);
  const styleCarouselRef = useRef<HTMLDivElement>(null);

  // Load history from localStorage
  useEffect(() => {
    const savedHistory = localStorage.getItem('caricature_history');
    if (savedHistory) {
      try {
        setHistory(JSON.parse(savedHistory));
      } catch (e) {
        console.error('Failed to load history:', e);
      }
    }
    
    // Show tutorial for first-time users
    const hasSeenTutorial = localStorage.getItem('caricature_tutorial_seen');
    if (!hasSeenTutorial) {
      setShowTutorial(true);
    }
  }, []);

  // Save history to localStorage
  useEffect(() => {
    localStorage.setItem('caricature_history', JSON.stringify(history));
  }, [history]);

  // Handle file selection
  const handleFileSelect = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      if (file.size > 10 * 1024 * 1024) {
        setError('Файл слишком большой. Максимум 10 МБ.');
        return;
      }
      
      const reader = new FileReader();
      reader.onload = (e) => {
        setSelectedImage(e.target?.result as string);
        setGeneratedImage(null);
        setError(null);
      };
      reader.readAsDataURL(file);
    }
  }, []);

  // Handle camera capture
  const handleCameraCapture = useCallback(() => {
    if (fileInputRef.current) {
      fileInputRef.current.setAttribute('capture', 'environment');
      fileInputRef.current.click();
    }
  }, []);

  // Handle gallery selection
  const handleGallerySelect = useCallback(() => {
    if (fileInputRef.current) {
      fileInputRef.current.removeAttribute('capture');
      fileInputRef.current.click();
    }
  }, []);

  // Generate caricature
  const handleGenerate = useCallback(async () => {
    if (!selectedImage) return;
    
    setIsGenerating(true);
    setError(null);
    
    try {
      const response = await fetch('/api/caricature', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          image: selectedImage.split(',')[1], // Remove data:image/...;base64, prefix
          style: selectedStyle,
          intensity,
        }),
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.error || 'Failed to generate caricature');
      }
      
      setGeneratedImage(`data:image/png;base64,${data.image}`);
      
      // Add to history
      const historyItem: HistoryItem = {
        id: Date.now().toString(),
        originalImage: selectedImage,
        caricatureImage: `data:image/png;base64,${data.image}`,
        style: selectedStyle,
        intensity,
        createdAt: Date.now(),
      };
      
      setHistory(prev => [historyItem, ...prev].slice(0, 20)); // Keep last 20 items
      
    } catch (err: any) {
      setError(err.message || 'Ошибка при генерации');
    } finally {
      setIsGenerating(false);
    }
  }, [selectedImage, selectedStyle, intensity]);

  // Download image
  const handleDownload = useCallback((imageData: string) => {
    const link = document.createElement('a');
    link.href = imageData;
    link.download = `caricature_${Date.now()}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }, []);

  // Share image
  const handleShare = useCallback(async (imageData: string) => {
    try {
      // Convert base64 to blob
      const response = await fetch(imageData);
      const blob = await response.blob();
      const file = new File([blob], 'caricature.png', { type: 'image/png' });
      
      if (navigator.share && navigator.canShare({ files: [file] })) {
        await navigator.share({
          files: [file],
          title: 'Мой шарж',
          text: 'Посмотри какой шарж я создал!',
        });
      } else {
        // Fallback: copy to clipboard or show download
        handleDownload(imageData);
      }
    } catch (err) {
      console.error('Share failed:', err);
      handleDownload(imageData);
    }
  }, [handleDownload]);

  // Delete from history
  const handleDeleteFromHistory = useCallback((id: string) => {
    setHistory(prev => prev.filter(item => item.id !== id));
  }, []);

  // Scroll style carousel
  const scrollStyle = useCallback((direction: 'left' | 'right') => {
    if (styleCarouselRef.current) {
      const scrollAmount = 200;
      styleCarouselRef.current.scrollBy({
        left: direction === 'left' ? -scrollAmount : scrollAmount,
        behavior: 'smooth',
      });
    }
  }, []);

  // Close tutorial
  const closeTutorial = useCallback(() => {
    setShowTutorial(false);
    localStorage.setItem('caricature_tutorial_seen', 'true');
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-950 via-violet-900 to-indigo-950 text-white">
      {/* Status bar spacer */}
      <div className="h-safe-top" />
      
      {/* Main content */}
      <main className="pb-20">
        {/* Header */}
        <header className="sticky top-0 z-40 bg-black/30 backdrop-blur-xl border-b border-white/10">
          <div className="px-4 py-3 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-pink-500 to-violet-600 flex items-center justify-center shadow-lg">
                <Wand2 className="w-5 h-5 text-white" />
              </div>
              <div>
                <h1 className="text-lg font-bold">ШаржМастер</h1>
                <p className="text-xs text-white/60">AI шаржи за секунды</p>
              </div>
            </div>
            <button 
              onClick={() => setShowTutorial(true)}
              className="p-2 rounded-full hover:bg-white/10 transition-colors"
            >
              <Info className="w-5 h-5 text-white/60" />
            </button>
          </div>
        </header>

        {/* Create Tab */}
        {activeTab === 'create' && (
          <div className="px-4 py-4 space-y-4">
            {/* Image Upload Area */}
            {!selectedImage ? (
              <motion.div 
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-white/5 border-2 border-dashed border-white/20 rounded-3xl p-8 text-center"
              >
                <div className="w-20 h-20 mx-auto mb-4 rounded-2xl bg-gradient-to-br from-pink-500/20 to-violet-500/20 flex items-center justify-center">
                  <ImagePlus className="w-10 h-10 text-pink-400" />
                </div>
                <h2 className="text-xl font-semibold mb-2">Загрузите фото</h2>
                <p className="text-white/60 text-sm mb-6">
                  Выберите фото из галереи или сделайте новое
                </p>
                <div className="flex gap-3 justify-center">
                  <motion.button
                    whileTap={{ scale: 0.95 }}
                    onClick={handleCameraCapture}
                    className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-pink-600 to-rose-600 rounded-xl font-medium shadow-lg shadow-pink-500/25"
                  >
                    <Camera className="w-5 h-5" />
                    Камера
                  </motion.button>
                  <motion.button
                    whileTap={{ scale: 0.95 }}
                    onClick={handleGallerySelect}
                    className="flex items-center gap-2 px-6 py-3 bg-white/10 rounded-xl font-medium border border-white/20"
                  >
                    <ImagePlus className="w-5 h-5" />
                    Галерея
                  </motion.button>
                </div>
              </motion.div>
            ) : (
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="space-y-4"
              >
                {/* Original Image */}
                <div className="relative rounded-2xl overflow-hidden bg-black/30">
                  <div className="absolute top-2 left-2 px-3 py-1 bg-black/50 rounded-full text-xs font-medium backdrop-blur-sm">
                    Оригинал
                  </div>
                  <img 
                    src={selectedImage} 
                    alt="Original" 
                    className="w-full aspect-square object-cover"
                    style={{ transform: `scale(${zoom})` }}
                  />
                  <button
                    onClick={() => {
                      setSelectedImage(null);
                      setGeneratedImage(null);
                    }}
                    className="absolute top-2 right-2 p-2 bg-black/50 rounded-full backdrop-blur-sm"
                  >
                    <X className="w-5 h-5" />
                  </button>
                  
                  {/* Zoom controls */}
                  <div className="absolute bottom-3 right-3 flex gap-2">
                    <button
                      onClick={() => setZoom(Math.max(1, zoom - 0.2))}
                      className="p-2 bg-black/50 rounded-full backdrop-blur-sm"
                    >
                      <ZoomOut className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => setZoom(Math.min(2, zoom + 0.2))}
                      className="p-2 bg-black/50 rounded-full backdrop-blur-sm"
                    >
                      <ZoomIn className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => setZoom(1)}
                      className="p-2 bg-black/50 rounded-full backdrop-blur-sm"
                    >
                      <RotateCcw className="w-4 h-4" />
                    </button>
                  </div>
                </div>
                
                {/* Style Selection */}
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <h3 className="font-semibold flex items-center gap-2">
                      <Palette className="w-4 h-4 text-pink-400" />
                      Стиль шаржа
                    </h3>
                    <div className="flex gap-1">
                      <button
                        onClick={() => scrollStyle('left')}
                        className="p-1.5 bg-white/10 rounded-full"
                      >
                        <ChevronLeft className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => scrollStyle('right')}
                        className="p-1.5 bg-white/10 rounded-full"
                      >
                        <ChevronRight className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                  
                  <div 
                    ref={styleCarouselRef}
                    className="flex gap-3 overflow-x-auto scrollbar-hide pb-2 -mx-4 px-4"
                    style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
                  >
                    {CARICATURE_STYLES.map((style) => (
                      <motion.button
                        key={style.id}
                        whileTap={{ scale: 0.95 }}
                        onClick={() => setSelectedStyle(style.id)}
                        className={cn(
                          "flex-shrink-0 p-3 rounded-2xl border-2 transition-all min-w-[100px]",
                          selectedStyle === style.id
                            ? "border-pink-500 bg-pink-500/20"
                            : "border-white/10 bg-white/5"
                        )}
                      >
                        <div className="text-2xl mb-1">{style.icon}</div>
                        <div className="text-sm font-medium">{style.nameRu}</div>
                      </motion.button>
                    ))}
                  </div>
                </div>
                
                {/* Intensity Slider */}
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <h3 className="font-semibold flex items-center gap-2">
                      <Sliders className="w-4 h-4 text-violet-400" />
                      Интенсивность
                    </h3>
                    <span className="text-sm text-white/60">{intensity}%</span>
                  </div>
                  <input
                    type="range"
                    min="10"
                    max="100"
                    value={intensity}
                    onChange={(e) => setIntensity(Number(e.target.value))}
                    className="w-full h-2 bg-white/10 rounded-full appearance-none cursor-pointer
                      [&::-webkit-slider-thumb]:appearance-none
                      [&::-webkit-slider-thumb]:w-6
                      [&::-webkit-slider-thumb]:h-6
                      [&::-webkit-slider-thumb]:rounded-full
                      [&::-webkit-slider-thumb]:bg-gradient-to-r
                      [&::-webkit-slider-thumb]:from-pink-500
                      [&::-webkit-slider-thumb]:to-violet-500
                      [&::-webkit-slider-thumb]:shadow-lg
                      [&::-webkit-slider-thumb]:shadow-pink-500/25"
                  />
                  <div className="flex justify-between text-xs text-white/40">
                    <span>Тонкий</span>
                    <span>Сильный</span>
                  </div>
                </div>
                
                {/* Generate Button */}
                <motion.button
                  whileTap={{ scale: 0.98 }}
                  onClick={handleGenerate}
                  disabled={isGenerating}
                  className={cn(
                    "w-full py-4 rounded-2xl font-semibold text-lg flex items-center justify-center gap-3 shadow-lg",
                    isGenerating
                      ? "bg-white/10 cursor-not-allowed"
                      : "bg-gradient-to-r from-pink-600 via-purple-600 to-violet-600 shadow-purple-500/25"
                  )}
                >
                  {isGenerating ? (
                    <>
                      <Loader2 className="w-6 h-6 animate-spin" />
                      Создаём шарж...
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-6 h-6" />
                      Создать шарж
                    </>
                  )}
                </motion.button>
                
                {/* Error Message */}
                {error && (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="p-4 bg-red-500/20 border border-red-500/50 rounded-xl text-red-200 text-sm"
                  >
                    {error}
                  </motion.div>
                )}
                
                {/* Generated Image */}
                {generatedImage && (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="space-y-3"
                  >
                    <div className="relative rounded-2xl overflow-hidden bg-black/30">
                      <div className="absolute top-2 left-2 px-3 py-1 bg-gradient-to-r from-pink-500 to-violet-500 rounded-full text-xs font-medium">
                        ✨ Шарж готов!
                      </div>
                      <img 
                        src={generatedImage} 
                        alt="Caricature" 
                        className="w-full aspect-square object-cover"
                      />
                    </div>
                    
                    {/* Action Buttons */}
                    <div className="flex gap-3">
                      <motion.button
                        whileTap={{ scale: 0.95 }}
                        onClick={() => handleDownload(generatedImage)}
                        className="flex-1 py-3 bg-white/10 rounded-xl font-medium flex items-center justify-center gap-2 border border-white/20"
                      >
                        <Download className="w-5 h-5" />
                        Скачать
                      </motion.button>
                      <motion.button
                        whileTap={{ scale: 0.95 }}
                        onClick={() => handleShare(generatedImage)}
                        className="flex-1 py-3 bg-gradient-to-r from-pink-600 to-violet-600 rounded-xl font-medium flex items-center justify-center gap-2"
                      >
                        <Share2 className="w-5 h-5" />
                        Поделиться
                      </motion.button>
                    </div>
                  </motion.div>
                )}
              </motion.div>
            )}
            
            {/* Hidden file input */}
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleFileSelect}
              className="hidden"
            />
          </div>
        )}

        {/* History Tab */}
        {activeTab === 'history' && (
          <div className="px-4 py-4">
            <h2 className="text-xl font-bold mb-4">История</h2>
            
            {history.length === 0 ? (
              <div className="text-center py-12">
                <div className="w-16 h-16 mx-auto mb-4 rounded-2xl bg-white/5 flex items-center justify-center">
                  <History className="w-8 h-8 text-white/40" />
                </div>
                <p className="text-white/60">История пуста</p>
                <p className="text-white/40 text-sm">Созданные шаржи появятся здесь</p>
              </div>
            ) : (
              <div className="grid grid-cols-2 gap-3">
                <AnimatePresence>
                  {history.map((item) => (
                    <motion.div
                      key={item.id}
                      initial={{ opacity: 0, scale: 0.9 }}
                      animate={{ opacity: 1, scale: 1 }}
                      exit={{ opacity: 0, scale: 0.9 }}
                      className="relative rounded-2xl overflow-hidden bg-black/30 aspect-square group"
                    >
                      <img 
                        src={item.caricatureImage} 
                        alt="Caricature"
                        className="w-full h-full object-cover"
                      />
                      <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity">
                        <div className="absolute bottom-0 left-0 right-0 p-3">
                          <div className="flex gap-2">
                            <button
                              onClick={() => handleDownload(item.caricatureImage)}
                              className="flex-1 p-2 bg-white/20 rounded-lg backdrop-blur-sm"
                            >
                              <Download className="w-4 h-4 mx-auto" />
                            </button>
                            <button
                              onClick={() => handleShare(item.caricatureImage)}
                              className="flex-1 p-2 bg-white/20 rounded-lg backdrop-blur-sm"
                            >
                              <Share2 className="w-4 h-4 mx-auto" />
                            </button>
                            <button
                              onClick={() => handleDeleteFromHistory(item.id)}
                              className="flex-1 p-2 bg-red-500/30 rounded-lg backdrop-blur-sm"
                            >
                              <Trash2 className="w-4 h-4 mx-auto" />
                            </button>
                          </div>
                        </div>
                      </div>
                      <div className="absolute top-2 left-2 px-2 py-1 bg-black/50 rounded-full text-xs backdrop-blur-sm">
                        {CARICATURE_STYLES.find(s => s.id === item.style)?.icon}
                      </div>
                    </motion.div>
                  ))}
                </AnimatePresence>
              </div>
            )}
            
            {history.length > 0 && (
              <button
                onClick={() => setHistory([])}
                className="w-full mt-4 py-3 bg-red-500/20 border border-red-500/50 rounded-xl text-red-300 text-sm"
              >
                Очистить историю
              </button>
            )}
          </div>
        )}

        {/* Profile Tab */}
        {activeTab === 'profile' && (
          <div className="px-4 py-4 space-y-4">
            <div className="text-center py-8">
              <div className="w-24 h-24 mx-auto mb-4 rounded-3xl bg-gradient-to-br from-pink-500 to-violet-600 flex items-center justify-center shadow-xl shadow-purple-500/25">
                <User className="w-12 h-12 text-white" />
              </div>
              <h2 className="text-2xl font-bold mb-1">ШаржМастер</h2>
              <p className="text-white/60">Версия 1.0</p>
            </div>
            
            <div className="space-y-3">
              <div className="p-4 bg-white/5 rounded-2xl border border-white/10">
                <div className="flex items-center justify-between">
                  <span className="text-white/60">Создано шаржей</span>
                  <span className="text-2xl font-bold text-pink-400">{history.length}</span>
                </div>
              </div>
              
              <div className="p-4 bg-white/5 rounded-2xl border border-white/10">
                <h3 className="font-semibold mb-2">О приложении</h3>
                <p className="text-sm text-white/60">
                  ШаржМастер использует искусственный интеллект для создания 
                  уникальных шаржей из ваших фотографий. Выберите стиль, 
                  настройте интенсивность и получите креативный портрет за секунды!
                </p>
              </div>
              
              <div className="p-4 bg-white/5 rounded-2xl border border-white/10">
                <h3 className="font-semibold mb-2">Возможности</h3>
                <ul className="text-sm text-white/60 space-y-1">
                  <li>✨ 7 уникальных стилей шаржей</li>
                  <li>📸 Загрузка из галереи или камеры</li>
                  <li>🎚️ Настраиваемая интенсивность</li>
                  <li>💾 История созданных шаржей</li>
                  <li>📤 Скачивание и обмен</li>
                </ul>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Bottom Navigation */}
      <nav className="fixed bottom-0 left-0 right-0 bg-black/40 backdrop-blur-xl border-t border-white/10 z-50">
        <div className="flex justify-around py-2 pb-safe">
          <button
            onClick={() => setActiveTab('create')}
            className={cn(
              "flex flex-col items-center py-2 px-6 rounded-xl transition-colors",
              activeTab === 'create' ? "text-pink-400" : "text-white/60"
            )}
          >
            <Wand2 className="w-6 h-6" />
            <span className="text-xs mt-1">Создать</span>
          </button>
          <button
            onClick={() => setActiveTab('history')}
            className={cn(
              "flex flex-col items-center py-2 px-6 rounded-xl transition-colors",
              activeTab === 'history' ? "text-pink-400" : "text-white/60"
            )}
          >
            <History className="w-6 h-6" />
            <span className="text-xs mt-1">История</span>
          </button>
          <button
            onClick={() => setActiveTab('profile')}
            className={cn(
              "flex flex-col items-center py-2 px-6 rounded-xl transition-colors",
              activeTab === 'profile' ? "text-pink-400" : "text-white/60"
            )}
          >
            <User className="w-6 h-6" />
            <span className="text-xs mt-1">Профиль</span>
          </button>
        </div>
      </nav>

      {/* Tutorial Modal */}
      <AnimatePresence>
        {showTutorial && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-6"
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="bg-gradient-to-br from-violet-900 to-purple-950 rounded-3xl p-6 max-w-sm w-full border border-white/20 shadow-2xl"
            >
              <div className="text-center">
                <div className="w-16 h-16 mx-auto mb-4 rounded-2xl bg-gradient-to-br from-pink-500 to-violet-600 flex items-center justify-center shadow-lg">
                  <Sparkles className="w-8 h-8 text-white" />
                </div>
                <h2 className="text-2xl font-bold mb-2">Добро пожаловать!</h2>
                <p className="text-white/70 mb-6">
                  Создавайте уникальные шаржи из ваших фотографий с помощью AI
                </p>
                
                <div className="space-y-3 text-left mb-6">
                  <div className="flex items-start gap-3">
                    <div className="w-8 h-8 rounded-lg bg-pink-500/20 flex items-center justify-center flex-shrink-0">
                      <span>1</span>
                    </div>
                    <div>
                      <div className="font-medium">Загрузите фото</div>
                      <div className="text-sm text-white/60">Из галереи или камеры</div>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <div className="w-8 h-8 rounded-lg bg-violet-500/20 flex items-center justify-center flex-shrink-0">
                      <span>2</span>
                    </div>
                    <div>
                      <div className="font-medium">Выберите стиль</div>
                      <div className="text-sm text-white/60">7 уникальных стилей на выбор</div>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <div className="w-8 h-8 rounded-lg bg-purple-500/20 flex items-center justify-center flex-shrink-0">
                      <span>3</span>
                    </div>
                    <div>
                      <div className="font-medium">Получите шарж!</div>
                      <div className="text-sm text-white/60">Скачайте или поделитесь</div>
                    </div>
                  </div>
                </div>
                
                <button
                  onClick={closeTutorial}
                  className="w-full py-3 bg-gradient-to-r from-pink-600 to-violet-600 rounded-xl font-semibold"
                >
                  Понятно!
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
