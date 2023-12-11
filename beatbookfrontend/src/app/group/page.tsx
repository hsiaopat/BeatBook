'use client'
import { useEffect, useState } from 'react';
import axios from 'axios';
import { useSearchParams } from 'next/navigation';
import Link from 'next/link';
import * as d3 from 'd3'; 



// Define the type for your group data
interface GroupData {
  group_id: string;
  group_name: string;
  num_members: number;
  group_members: string[];
  features: number[];
  feature_diff: number[];
  shared_artists: { 'Artist Name': string }[];
  artists_pie: { 'Artist Name': string; 'Num Songs': number; 'Percent Top Songs': number }[];
  shared_tracks: { 'Track Name': string; 'Artist Name': string; 'Album Name': string }[];
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

const createPieChart = (data: { 'Artist Name': string; 'Num Songs': number; 'Percent Top Songs': number }[]) => {
  const width = 800;
  const height = 400;
  const radius = Math.min(width, height) / 2;

  // Create an svg element for the pie chart and key
  const svg = d3.select('#pieChart').append('svg').attr('width', width).attr('height', height);

  // Create a group for the pie chart
  const pieGroup = svg.append('g').attr('transform', `translate(${width / 3},${height / 2})`);

  // Create a pie chart
  const pie = d3.pie<{ 'Artist Name': string; 'Num Songs': number; 'Percent Top Songs': number }>().value((d) => d['Percent Top Songs']);
  const data_ready = pie(data) as Array<d3.PieArcDatum<{ 'Artist Name': string; 'Num Songs': number; 'Percent Top Songs': number }>>;

  // Create arcs
  const arc = d3.arc<d3.PieArcDatum<{ 'Artist Name': string; 'Num Songs': number; 'Percent Top Songs': number }>>().innerRadius(0).outerRadius(radius);

  // Add slices to the pie chart
  const color = d3.scaleOrdinal(d3.schemeCategory10);
  pieGroup
    .selectAll('slices')
    .data(data_ready)
    .enter()
    .append('path')
    .attr('d', arc)
    .attr('fill', (d) => color(d.data['Artist Name']));

  // Create a group for the key
  const keyGroup = svg.append('g').attr('transform', `translate(${width / 1.5},${height / 4})`);

  // Add key entries
  const keyEntries = keyGroup
    .selectAll('keyEntries')
    .data(data_ready)
    .enter()
    .append('g')
    .attr('transform', (d, i) => `translate(0,${i * 20})`);

  keyEntries
    .append('rect')
    .attr('width', 15)
    .attr('height', 15)
    .attr('fill', (d) => color(d.data['Artist Name']));

  keyEntries
    .append('text')
    .text((d) => `${d.data['Artist Name']} (${d.data['Percent Top Songs']}%)`)
    .attr('x', 20)
    .attr('y', 10)
    .style('font-size', '12px')
    .style('fill', 'black');
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

 useEffect(() => {
  // Check if group data is available and artists_pie is present
  if (group && group.artists_pie) {
    // Create a pie chart
    createPieChart(group.artists_pie);
  }
}, [group]);


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

        <div className="bg-white p-8 rounded-md shadow-md">
  <h1 className="text-2xl font-bold mb-4">Group ID: {group.group_id}</h1>
  <p className="text-lg">Group Name: {group.group_name}</p>

  <div className="mt-6">
    <h2 className="text-3xl font-bold mb-4">Group Members</h2>
    <ul className="list-disc pl-6">
      {group.group_members.map((member, index) => (
        <li key={index} className="mb-2">{member}</li>
      ))}
    </ul>
  </div>
  </div>

  <div className="sm:flex items-center justify-center max-w-screen-xl h-screen">
  <div className="sm:w-1/2 p-5 text-center">
    <div className="text">
      <span className="text-gray-500 border-b-2 border-blue-600 uppercase">What is this?</span>
      <h2 className="my-4 font-bold text-3xl sm:text-4xl">About <span className="text-blue-600">Dorm Party/Wrapped</span></h2>
      <p className="text-gray-700">
        Take a sneak peek into Dorm Party and Dorm Wrapped! Click the button below to view your dorm party in your own Spotify library! We used a clustering algorithm to find songs perfectly catered to you and your friends! 
        Scroll down to look at your group stats and see your Dorm Wrapped!
      </p>
    </div>
  </div>
</div>

    

        
        

    {/* Make Cluster recommendation playlist*/}

  <h2 className="my-4 font-bold text-4xl sm:text-4xl">Dorm Wrapped</h2>

    {/* Artist Pie */}
    <h2 className="text-3xl font-bold mb-4">Artist Listening Distribution</h2>
    <div className="mt-8">
    <div className="text-3xl font-bold mb-4 mx-auto" id="pieChart" style={{ margin: '20px auto' }}></div>
    </div>
     {/* Add more details about the group as needed */}
    {/*Shared Artists*/}
     <div className="mt-8">
        <h2 className="text-3xl font-bold mb-4">Shared Artists</h2>
        <ul className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {group.shared_artists.map((artist) => (
            <li key={artist['Artist Name']} className="bg-blue-100 p-4 rounded-md">
              {artist['Artist Name']}
            </li>
          ))}
        </ul>
      </div>

      {/* Unique Tracks Section */}
      <div className="mt-8">
        <h2 className="text-3xl font-bold mb-4">Shared Tracks</h2>
        <ul className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {group.shared_tracks.map((track, index) => (
            <li key={index} className="bg-green-100 p-4 rounded-md">
              <strong>{track['Track Name']}</strong> - {track['Artist Name']} - {track['Album Name']}
            </li>
          ))}
        </ul>
      </div>
      <p>Features: {JSON.stringify(group.features)}</p>
      <p>Feature Diff: {JSON.stringify(group.feature_diff)}</p>

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