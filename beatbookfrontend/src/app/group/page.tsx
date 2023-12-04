'use client'
// GroupPage.tsx
import { useEffect, useState } from 'react';
import axios from 'axios';

const GroupPage: React.FC = () => {
  const [group, setGroup] = useState<any>(null);

  useEffect(() => {
    const fetchGroupDetails = async () => {
      try {
        // Extract group_id from the current URL
        const urlParams = new URLSearchParams(window.location.search);
        const group_id = urlParams.get('group_id');

        if (!group_id) {
          console.error('Group ID not found in the URL');
          // Handle the case where group_id is not present in the URL
          return;
        }

        // Fetch group details using the extracted group_id
        const response = await axios.get(`http://129.74.153.235:5028/group/${group_id}`);
        const groupData = response.data.group;

        // Set the group state with the fetched data
        setGroup(groupData);
      } catch (error) {
        console.error('Error fetching group details:', error);
        // Handle error as needed
      }
    };

    // Fetch group details when the component mounts
    fetchGroupDetails();
  }, []); // Empty dependency array ensures the effect runs only once on mount

  if (!group) {
    return <p>Loading group details...</p>;
  }

  return (
    <div>
      <h1>Group ID: {group.group_id}</h1>
      <p>Group Name: {group.group_name}</p>
      <p>Members: {group.num_members}</p>
      {/* Add more details about the group as needed */}
    </div>
  );
};

export default GroupPage;
