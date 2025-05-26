import React, { useState } from 'react';
import { Copy, Check, RotateCcw } from 'lucide-react';
import '../styles/ResultsView.css';

function ResultsView({ croppedImage, extractedText, onReset }) {
  const [copied, setCopied] = useState(false);
  
  const handleCopyText = () => {
    navigator.clipboard.writeText(extractedText)
      .then(() => {
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
      })
      .catch(err => {
        console.error('Failed to copy text: ', err);
      });
  };

  return (
    <div className="results-container">
      <div className="results-header">
        <h2>Extracted Text Results</h2>
        <button className="reset-button" onClick={onReset}>
          <RotateCcw size={16} />
          Start Over
        </button>
      </div>
      
      <div className="results-content">
        <div className="image-section">
          <h3>Selected Image Area</h3>
          <div className="image-preview">
            <img src={croppedImage} alt="Selected area" />
          </div>
        </div>
        
        <div className="text-section">
          <div className="text-header">
            <h3>Extracted Text</h3>
            <button 
              className={`copy-button ${copied ? 'copied' : ''}`}
              onClick={handleCopyText}
            >
              {copied ? <Check size={16} /> : <Copy size={16} />}
              {copied ? 'Copied!' : 'Copy Text'}
            </button>
          </div>
          
          <div className="extracted-text">
            {extractedText ? 
              <p>{extractedText}</p> : 
              <p className="no-text">No text was extracted from the selected area.</p>
            }
          </div>
        </div>
      </div>
    </div>
  );
}

export default ResultsView;