import React from 'react';

const EcoTrackLogo = ({ width = 200, height = 80 }) => {
  const styles = {
    text: {
      fontFamily: 'Arial, sans-serif',
      fontSize: '24px',
      fontWeight: 'bold',
      fill: '#fff'
    }
  };

  return (
    <svg
      width={width}
      height={height}
      viewBox="0 0 200 80"
      xmlns="http://www.w3.org/2000/svg"
    >
      <defs>
        <linearGradient id="leafGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#4CAF50" />
          <stop offset="100%" stopColor="#2E7D32" />
        </linearGradient>
      </defs>
      
      {/* Leaf shape */}
      <path
        d="M40,60 Q60,40 80,20 T120,40 Q100,60 80,70 Q60,80 40,60 Z"
        fill="url(#leafGradient)"
      />
      
      {/* Line graph */}
      <polyline
        points="40,60 60,40 80,50 100,30 120,40"
        fill="none"
        stroke="#FFFFFF"
        strokeWidth="3"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      
      {/* Company name */}
      <text x="10" y="75" style={styles.text}>
        EcoTrack
      </text>
    </svg>
  );
};

export default EcoTrackLogo;