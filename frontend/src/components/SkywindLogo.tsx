import React from 'react';
import './SkywindLogo.css';

interface SkywindLogoProps {
  size?: 'small' | 'medium' | 'large';
  showText?: boolean;
  variant?: 'light' | 'dark';
}

const SkywindLogo: React.FC<SkywindLogoProps> = ({
  size = 'medium',
  showText = false, // Default to false since the logo image includes text
  variant = 'light'
}) => {
  const sizeMap = {
    small: { height: 28 },
    medium: { height: 36 },
    large: { height: 44 },
  };

  const { height } = sizeMap[size];

  return (
    <div className={`skywind-logo skywind-logo-${size} skywind-logo-${variant}`}>
      <img
        src="/assets/skywind-logo.png"
        alt="Skywind Software Group"
        className="skywind-logo-img"
      />
    </div>
  );
};

export default SkywindLogo;
