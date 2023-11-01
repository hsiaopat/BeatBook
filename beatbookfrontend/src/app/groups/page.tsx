'use client'
import React, { useEffect } from 'react';
import Button from '@mui/material/Button';
import axios from 'axios';
import Header from '../components/header';

const GroupsPage: React.FC = () => {
  const handleJoinGroup = async () => {
    try {
      const spotifyAuthUrl = 'http://129.74.153.235:5028/join-group';
      window.location.href = spotifyAuthUrl;
      //const response = await axios.post('/join-group');
      //console.log(response.data);
      // add code to update UI or perform additional actions after joining
    } catch (error) {
      console.error(error);
    }
  };

  const handleCreateGroup = async () => {
    try {
      const spotifyAuthUrl = 'http://129.74.153.235:5028/create-group';
      window.location.href = spotifyAuthUrl;
      //const response = await axios.post('/join-group');
      //console.log(response.data);
      // add code to update UI or perform additional actions after joining
    } catch (error) {
      console.error(error);
    }
  };

  const handleLeaveGroup = async () => {
    try {
      const response = await axios.post('/leave-group');
      console.log(response.data);
      // add code to update UI or perform additional actions after leaving
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    // This effect runs only on the client side
    const handleJoinGroupClient = () => {
      handleJoinGroup();
    };

    const handleLeaveGroupClient = () => {
      handleLeaveGroup();
    };

    const handleCreateGroupClient = () => {
      handleCreateGroup();
    };

    // Attach the client-side event handlers
    document.getElementById('joinGroupButton')?.addEventListener('click', handleJoinGroupClient);
    document.getElementById('leaveGroupButton')?.addEventListener('click', handleLeaveGroupClient);
    document.getElementById('createGroupButton')?.addEventListener('click', handleCreateGroupClient);

    // Clean up the event handlers when the component unmounts
    return () => {
      document.getElementById('joinGroupButton')?.removeEventListener('click', handleJoinGroupClient);
      document.getElementById('leaveGroupButton')?.removeEventListener('click', handleLeaveGroupClient);
      document.getElementById('createGroupButton')?.removeEventListener('click', handleCreateGroupClient);

    };
  }, []); // Empty dependency array ensures the effect runs only once on mount

  return (
    <div className="dark">
      <Header />
      <div className="bg-spotify-dark min-h-screen flex flex-col items-center justify-center text-spotify-white">
        <div className="space-x-4">
        <Button
          id="joinGroupButton"
          variant="contained"
         >
        Join Group
      </Button>

          <Button
            id="createGroupButton"
            variant="contained"
          >
            Create Group
          </Button>

          <Button
            id="leaveGroupButton"
            variant="contained"
          >
            Leave Group
          </Button>

        </div>
      </div>
    </div>
  );
};

export default GroupsPage;
