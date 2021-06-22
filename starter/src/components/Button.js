import React from 'react';
import './Button.css';
import { Link } from 'react-router-dom';

const STYLES = ['btn--primary','btn--outline','btn--rounded']

const SIZES = ['btn--medium','btn--large']

export const Button = ({
    children,
    onClick,
    buttonStyle,
    buttonSize,
    hasNextLink,
    nextLink,
  }) => {
    const checkButtonStyle = STYLES.includes(buttonStyle)
      ? buttonStyle
      : STYLES[0];
  
    const checkButtonSize = SIZES.includes(buttonSize) ? buttonSize : SIZES[0];
  
    return (
        hasNextLink?
        <Link to={nextLink} className='btn--mobile'>
            <button
                className={`btn ${checkButtonStyle} ${checkButtonSize}`}
                onClick={() => onClick()}
            >
                {children}
            </button>
        </Link>:
        <button
            className={`btn ${checkButtonStyle} ${checkButtonSize}`}
            onClick={() => onClick()}
        >
            {children}
        </button>

    );
  };