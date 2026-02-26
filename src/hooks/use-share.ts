'use client';

import { useCallback, useState } from 'react';

export function useShare() {
  const [isSharing, setIsSharing] = useState(false);

  const shareImage = useCallback(async (imageData: string, title: string = 'My Caricature') => {
    setIsSharing(true);
    try {
      // Convert base64 to blob
      const response = await fetch(imageData);
      const blob = await response.blob();
      const file = new File([blob], 'caricature.jpg', { type: 'image/jpeg' });

      // Check if Web Share API is available
      if (navigator.share && navigator.canShare({ files: [file] })) {
        await navigator.share({
          title,
          text: 'Check out my caricature!',
          files: [file],
        });
      } else {
        // Fallback: copy image to clipboard
        try {
          await navigator.clipboard.write([
            new ClipboardItem({ 'image/jpeg': blob }),
          ]);
          return { success: true, message: 'Image copied to clipboard!' };
        } catch {
          // Last fallback: download the image
          const url = URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = 'caricature.jpg';
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
          URL.revokeObjectURL(url);
          return { success: true, message: 'Image downloaded!' };
        }
      }
      return { success: true, message: 'Shared successfully!' };
    } catch (error) {
      console.error('Share error:', error);
      return { success: false, message: 'Failed to share image' };
    } finally {
      setIsSharing(false);
    }
  }, []);

  const downloadImage = useCallback((imageData: string, filename: string = 'caricature.jpg') => {
    const link = document.createElement('a');
    link.href = imageData;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }, []);

  return {
    isSharing,
    shareImage,
    downloadImage,
  };
}
