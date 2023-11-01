'use client'
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const TopTracksPage = () => {
    const [topTracks, setTopTracks] = useState([]);

    useEffect(() => {

        const fetchTopTracks = async () => {
            try {
                const response = await axios.get('http://129.74.153.235:5028/toptracks');
                console.log('Full Response:', response.data);
                setTopTracks(response.data.tracks);
            } catch (error) {
                console.error(error);
            }
        };

        fetchTopTracks();
    }, []); // Empty dependency array ensures the effect runs only once on mount

    return (
        <div>
            <h1>Top Tracks</h1>
            <ul>
                {topTracks.map((track, index) => (
                    <li key={index}>{track}</li>
                ))}
            </ul>
        </div>
    );
};

export default TopTracksPage;
