import React from 'react';

export function Button({ children, className = '', variant = 'primary', ...props }) {
    const variants = {
        primary: 'bg-primary text-white hover:bg-primary-700',
        secondary: 'bg-secondary text-white hover:bg-secondary-700',
    };

    return (
        <button
            className={`px-4 py-2 rounded ${variants[variant] || variants.primary} ${className}`}
            {...props}
        >
            {children}
        </button>
    );
}
