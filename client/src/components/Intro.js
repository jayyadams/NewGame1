import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Intro = () => {
    const navigate = useNavigate();
    const [currentStage, setCurrentStage] = useState(0);
    const [showStartButton, setShowStartButton] = useState(false);

    const storyText = [
        "Legends says theres a tower, so steep no man could climb...",
        "One so dangerous no one would dare walk...",
        "Littered with monsters and demons...",
        "Some say a god rules the tower from the top....",
        "To become a god you have to defeat a god...... can you do it?"
    ];

    useEffect(() => {
        if (currentStage < storyText.length) {
            const timer = setTimeout(() => {
                setCurrentStage(currentStage + 1);
            }, 3000);
            return () => clearTimeout(timer);
        } else if (!showStartButton) {
            const buttonTimer = setTimeout(() => {
                setShowStartButton(true);
            }, 7000);
            return () => clearTimeout(buttonTimer);
        }
    }, [currentStage, showStartButton, storyText.length]);

    const handleStartGame = async () => {
        try {
            const response = await axios.post(`/character_seen_intro`);
            console.log(response.data.message);
            navigate('/home');
        } catch (error) {
            console.error('Error updating intro status:', error);
        }
    };

    return (
        <div className="intro-container">
            <h1>Dan Machi</h1>
            {storyText.slice(0, currentStage).map((line, index) => (
                <p key={index} className="intro-line" style={{ animationDelay: `${index * 2}s` }}>{line}</p>
            ))}
            {showStartButton && (
                <button onClick={handleStartGame} className="intro-button">Start Game</button>
            )}
        </div>
    );
};

export default Intro;