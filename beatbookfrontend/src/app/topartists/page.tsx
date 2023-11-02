'use client'
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const TopArtistsPage = () => {
    const [topArtists, setTopArtists] = useState([]);

    useEffect(() => {

        const fetchTopTracks = async () => {
            try {
                const response = await axios.get('http://129.74.153.235:5028/topartists');
                console.log('Full Response:', response.data);
                setTopArtists(response.data.artists);
            } catch (error) {
                console.error(error);
            }
        };

        fetchTopTracks();
    }, []); // Empty dependency array ensures the effect runs only once on mount

    return (
        <div>
            <h1>Top Artists</h1>
            <ul>
                {topArtists.map((artist, index) => (
                    <li key={index}>{artist}</li>
                ))}
            </ul>
        </div>
    );
};

export default TopArtistsPage;
