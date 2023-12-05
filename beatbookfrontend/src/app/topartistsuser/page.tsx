'use client'
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { styled } from '@mui/system';

const Container = styled('div')({
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'flex-start',
  alignItems: 'center',
  height: '100vh',
}); 


const Title = styled('h1')({
  fontSize: '2rem',
  color: 'black',
  margin: 0,
  textAlign: 'center',

});

const CenteredButtons = styled('div')({
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  flex: 1,
});


const WelcomeMessage = styled('div')({
  backgroundColor: 'white', // Change the background color to pale green
  border: '1px solid black',
  padding: '1rem',
  textAlign: 'center',
  width: '35%',
  marginTop: '1rem', // Move closer to the black line
});




const TopArtistsUserPage = () => {
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

  const redirectToSpotify = async () => {
    try {
      const spotifyAuthUrl = 'http://129.74.153.235:5028/login';
      window.location.href = spotifyAuthUrl;
    } catch (error) {
      console.error('Error initiating Spotify login:', error);
    }
  };

  return (
<>
    <nav className="bg-white border-gray-200 dark:bg-gray-900">
      <div className="flex flex-wrap justify-between items-center mx-auto max-w-screen-xl p-4">
        <a href="https://spotify.com" className="flex items-center space-x-3 rtl:space-x-reverse">
          <span className="self-center text-2xl font-semibold whitespace-nowrap dark:text-white">BeatBook</span>
        </a>
        <div className="flex items-center space-x-6 rtl:space-x-reverse">
          <a href="#" className="text-sm text-blue-600 dark:text-blue-500 hover:underline" onClick={redirectToSpotify}>Login</a>
        </div>
      </div>
    </nav>
    <CenteredButtons>
    <Title>Top Artists</Title>
      <WelcomeMessage>
          Your Top 50 Artists:
          {topArtists.map((artist, index) => (
                    <li key={index}>{artist}</li>
                ))}
      </WelcomeMessage>
      </CenteredButtons>


    </>
  );
};

export default TopArtistsUserPage;


