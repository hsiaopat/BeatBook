'use client'
import React, { useEffect, useState } from 'react';
import axios from 'axios';


const TopArtistsPage = () => {
   const [topArtists, setTopArtists] = useState([]);


   const redirectToSpotify = async () => {
       try {
         const spotifyAuthUrl = 'http://129.74.153.235:5028/login';
         window.location.href = spotifyAuthUrl;
       } catch (error) {
         console.error('Error initiating Spotify login:', error);
       }
     };


   useEffect(() => {


       const fetchTopArtists = async () => {
           try {
               const response = await axios.get('http://129.74.153.235:5028/topartists');
               console.log('Full Response:', response.data);
               setTopArtists(response.data.artists);
           } catch (error) {
               console.error(error);
           }
       };


       fetchTopArtists();
   }, []); // Empty dependency array ensures the effect runs only once on mount


   return (
       <div>
           <nav className="bg-white border-gray-200 dark:bg-gray-900">
          <div className="flex flex-wrap justify-between items-center mx-auto max-w-screen-xl p-4">
            <a href="/home" className="flex items-center space-x-3 rtl:space-x-reverse">
              <span className="self-center text-2xl font-semibold whitespace-nowrap dark:text-white">BeatBook</span>
            </a>
            <div className="flex items-center space-x-6 rtl:space-x-reverse">
              <a className="text-sm text-blue-600 dark:text-blue-500 hover:underline" onClick={redirectToSpotify}>Login</a>
            </div>
          </div>
        </nav>




        <div className="mx-auto max-w-screen-xl flex flex-col items-center justify-center mt-4">
  <span className="text-sm font-semibold text-black dark:text-black-400"></span>
  <h2 className="mt-2 mb-4 text-2xl font-bold text-black dark:text-black-300">
    Your Top Artists
  </h2>
  <p className="mb-4 text-base leading-7 text-black dark:text-black-400">
    Take a look at your top 50 artists from the last 30 days. Tune In!
  </p>
  <ul className="mb-10">
    {topArtists.map((artist, index) => (
      <li key={index} className="flex items-center mb-4 text-base text-black dark:text-black-400">
        <span className="mr-3 text-blue-500 dark:text-blue-400">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
            className={`w-6 h-6 text-blue-500 dark:text-blue-400 bi bi-${index + 1}-circle-fill`} viewBox="0 0 16 16">
            {/* Path content */ }
          </svg>
        </span>
        {artist}
      </li>
    ))}
  </ul>
</div>



       </div>
   );
};


export default TopArtistsPage;
