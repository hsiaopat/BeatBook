'use client'
import { useEffect, useState } from 'react';
import axios from 'axios';
import { useSearchParams } from 'next/navigation';
import Link from 'next/link';



// Define the type for your group data
interface GroupData {
  group_id: string;
  group_name: string;
  num_members: number;
  features: number[];
  feature_diff: number[];
  shared_artists: { 'Artist Name': string }[];
  artists_pie: { 'Artist Name': string; 'Percent Top Songs': number }[];
  unique_tracks: { 'Track Name': string; 'Artist Name': string; 'Album Name': string }[];
  // Add more properties as needed
}


const GroupPage: React.FC = () => {
 const [group, setGroup] = useState<GroupData | null>(null);
 const [loading, setLoading] = useState(true);
 const searchParams = useSearchParams();


 const redirectToSpotify = async () => {
   try {
     const spotifyAuthUrl = 'http://129.74.153.235:5028/login';
     window.location.href = spotifyAuthUrl;
   } catch (error) {
     console.error('Error initiating Spotify login:', error);
   }
 };


 const handleCreateDormParty = async () => {
  try {
    // Prompt the user for the group name (you can use a prompt, input field, etc.)
    const groupParams: [string, string][] = Array.from(searchParams.entries());
    const group_id = groupParams.find(([key]) => key === 'group_id')?.[1];


    // Make the POST request with the group_name parameter
    const response = await axios.get(`http://129.74.153.235:5028/createDormParty/${group_id}`);
    console.log(response.data);
    // add code to update UI or perform additional actions after creating
  } catch (error) {
    console.error(error);
  }
};


 useEffect(() => {
   const fetchGroupDetails = async () => {
     try {
       const groupParams: [string, string][] = Array.from(searchParams.entries());
       const group_id = groupParams.find(([key]) => key === 'group_id')?.[1];


       if (!group_id) {
         console.error('Group ID not found in the URL');
         return;
       }


       const response = await axios.get(`http://129.74.153.235:5028/group/${group_id}`);
       const groupData: GroupData = response.data.group;


       setGroup(groupData);
       setLoading(false); // Set loading to false when data is loaded
     } catch (error) {
       console.error('Error fetching group details:', error);
       setLoading(false); // Set loading to false in case of an error
     }
   };


   // Fetch group details when the component mounts or when the dynamic route parameters change
   fetchGroupDetails();
 }, [searchParams]); // Dependency on the searchParams


 if (loading) {
   return <p>Loading group details...</p>;
 }


 if (!group) {
   return <p>Error loading group details.</p>;
 }


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
     <h1>Group ID: {group.group_id}</h1>
     <p>Group Name: {group.group_name}</p>
     <p>Members: {group.num_members}</p>
     <p>hello</p>

    {/* Make Cluster recommendation playlist*/}



    <div data-hs-carousel='{"loadingClasses": "opacity-0","isAutoPlay": true}' className="relative">
      <div className="hs-carousel relative overflow-hidden w-full min-h-[350px] bg-white rounded-lg">
        <div className="hs-carousel-body absolute top-0 bottom-0 start-0 flex flex-nowrap transition-transform duration-700 opacity-0">
          <div className="hs-carousel-slide">
            <div className="flex flex-col justify-center h-full bg-gray-100 p-6">
              <p className = "text-sm text-black-600">Features: {JSON.stringify(group.features)}</p>
            </div>
          </div>
          <div className="hs-carousel-slide">
            <div className="flex flex-col justify-center h-full bg-gray-200 p-6">
              <p>Feature Diff: {JSON.stringify(group.feature_diff)}</p>
            </div>
          </div>
          <div className="hs-carousel-slide">
            <div className="flex flex-col justify-center h-full bg-gray-300 p-6">
              <p>Shared Artists: {JSON.stringify(group.shared_artists)}</p>
            </div>
          </div>
          <div className="hs-carousel-slide">
            <div className="flex flex-col justify-center h-full bg-gray-400 p-6">
              <p>Artists Pie: {JSON.stringify(group.artists_pie)}</p>
            </div>
          </div>
          <div className="hs-carousel-slide">
            <div className="flex flex-col justify-center h-full bg-gray-500 p-6">
              <p>Unique Tracks: {JSON.stringify(group.unique_tracks)}</p>
            </div>
          </div>
        </div>
      </div>

      <button
        type="button"
        className="hs-carousel-prev hs-carousel:disabled:opacity-50 disabled:pointer-events-none absolute inset-y-0 start-0 inline-flex justify-center items-center w-[46px] h-full text-gray-800 hover:bg-gray-800/[.1]"
      >
        <span className="text-2xl" aria-hidden="true">
          <svg
            className="w-4 h-4"
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            fill="currentColor"
            viewBox="0 0 16 16"
          >
            <path fillRule="evenodd" d="M11.354 1.646a.5.5 0 0 1 0 .708L5.707 8l5.647 5.646a.5.5 0 0 1-.708.708l-6-6a.5.5 0 0 1 0-.708l6-6a.5.5 0 0 1 .708 0z" />
          </svg>
        </span>
        <span className="sr-only">Previous</span>
      </button>
      <button
        type="button"
        className="hs-carousel-next hs-carousel:disabled:opacity-50 disabled:pointer-events-none absolute inset-y-0 end-0 inline-flex justify-center items-center w-[46px] h-full text-gray-800 hover:bg-gray-800/[.1]"
      >
        <span className="sr-only">Next</span>
        <span className="text-2xl" aria-hidden="true">
          <svg
            className="w-4 h-4"
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            fill="currentColor"
            viewBox="0 0 16 16"
          >
            <path fillRule="evenodd" d="M4.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L10.293 8 4.646 2.354a.5.5 0 0 1 0-.708z" />
          </svg>
        </span>
      </button>

      <div className="hs-carousel-pagination flex justify-center absolute bottom-3 start-0 end-0 space-x-2">
      <span className="hs-carousel-active:bg-blue-700 hs-carousel-active:border-blue-700 w-3 h-3 border border-gray-400 rounded-full cursor-pointer"></span>
        <span className="hs-carousel-active:bg-blue-700 hs-carousel-active:border-blue-700 w-3 h-3 border border-gray-400 rounded-full cursor-pointer"></span>
        <span className="hs-carousel-active:bg-blue-700 hs-carousel-active:border-blue-700 w-3 h-3 border border-gray-400 rounded-full cursor-pointer"></span>
      </div>
    </div>

     {/* Add more details about the group as needed */}
      <p>Features: {JSON.stringify(group.features)}</p>
      <p>Feature Diff: {JSON.stringify(group.feature_diff)}</p>
      <p>Shared Artists: {JSON.stringify(group.shared_artists)}</p>
      <p>Artists Pie: {JSON.stringify(group.artists_pie)}</p>
      <p>Unique Tracks: {JSON.stringify(group.unique_tracks)}</p>

      <div className="flex justify-between items-center">
      {/* Container 1 */}
      <Link href="/">
        <a>
          <div className="flex flex-col items-center border border-gray-300 p-4 rounded-md hover:shadow-lg transition-transform duration-300 transform hover:scale-105 cursor-pointer w-64 h-48">
            <div className="bg-blue-600 text-white p-4 rounded-md">
              Dorm Party
            </div>
            <p className="text-gray-600 mt-2">Explore your BeatBook with DormParty!</p>
          </div>
        </a>
      </Link>
   </div>
  </div>
   
 );
};


export default GroupPage;