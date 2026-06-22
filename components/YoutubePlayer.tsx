'use client';
import YouTube from 'react-youtube';

interface YouTubePlayerProps {
  videoId: string;
}

function YouTubePlayer({ videoId }: YouTubePlayerProps) {
  const onError = (error: any) => {
    console.error('YouTube Player Error:', error);
  };

  return (
    <YouTube
      videoId={videoId}
      onError={onError}
      className="justify-center lg:justify-end lg:group-even/section:justify-start rounded-2xl mx-auto lg:mx-0"
    />
  );
}

export default YouTubePlayer;
