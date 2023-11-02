'use client'
import React, { useEffect, useState } from 'react';
import Button from '@mui/material/Button';
import axios from 'axios';
import Header from '../components/header';

interface Group {
  group_id: number;
  group_name: string;
  num_members: number;
}

const GroupsPage: React.FC = () => {
  const [groups, setGroups] = useState<Group[]>([]);

  const handleDisplayGroups = async () => {
    try {
      const response = await axios.get('http://129.74.153.235:5028/displaygroups');
      console.log('Response data:', response.data);
  
      // Check if the 'groups' property exists and is an array
      if (Array.isArray(response.data.groups)) {
        const transformedGroups: Group[] = response.data.groups.map((groupData: any) => ({
          group_id: groupData[0],
          group_name: groupData[1],
          num_members: groupData[2],
        }));
        console.log(transformedGroups);
        setGroups(transformedGroups || []);
      } else {
        console.error('Unexpected data structure:', response.data);
      }
    } catch (error) {
      console.error(error);
    }
  };
  
  
  const handleJoinGroup = async () => {
    try {
      const group_identifier = prompt('What group would you like to join? (group number or name)')
      if(!group_identifier){
        //handle case where group_name is not provided
        console.error('Group name not provided');
        return;
      }
      const response = await axios.post('http://129.74.153.235:5028/joingroup', { group_identifier });
      console.log(response.data);
      // add code to update UI or perform additional actions after joining
    } catch (error) {
      console.error(error);
    }
  };

  const handleCreateGroup = async () => {
    try {
      // Prompt the user for the group name (you can use a prompt, input field, etc.)
      const group_name = prompt('Enter group name:');
      if (!group_name) {
        // Handle case where group_name is not provided
        console.error('Group name not provided');
        return;
      }

      // Make the POST request with the group_name parameter
      const response = await axios.post('http://129.74.153.235:5028/creategroup', { group_name });
      console.log(response.data);
      // add code to update UI or perform additional actions after creating
    } catch (error) {
      console.error(error);
    }
  };

  const handleLeaveGroup = async () => {
    try {
      const group_identifier = prompt('What group would you like to leave? (group number or name)')
      if(!group_identifier){
        //handle case where group_name is not provided
        console.error('Group name not provided');
        return;
      }
      const response = await axios.post('http://129.74.153.235:5028/leavegroup', { group_identifier });
      console.log(response.data);
      // add code to update UI or perform additional actions after joining
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    const handleJoinGroupClient = () => {
      handleJoinGroup();
    };

    const handleLeaveGroupClient = () => {
      handleLeaveGroup();
    };

    const handleCreateGroupClient = () => {
      handleCreateGroup();
    };

    document.getElementById('joinGroupButton')?.addEventListener('click', handleJoinGroupClient);
    document.getElementById('leaveGroupButton')?.addEventListener('click', handleLeaveGroupClient);
    document.getElementById('createGroupButton')?.addEventListener('click', handleCreateGroupClient);
    handleDisplayGroups();

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
          <Button id="joinGroupButton" variant="contained">
            Join Group
          </Button>
  
          <Button id="createGroupButton" variant="contained">
            Create Group
          </Button>
  
          <Button id="leaveGroupButton" variant="contained">
            Leave Group
          </Button>
  
          {/* Display groups */}
          <div>
            <h2>Groups:</h2>
            <ul>
              {/* Iterate over each group and render a list item */}
              {groups.map((group) => (
                <li key={group.group_id}>{`${group.group_name} - Members: ${group.num_members}`}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GroupsPage;
