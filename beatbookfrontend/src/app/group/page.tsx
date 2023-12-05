'use client'
import { useEffect, useState } from 'react';
import axios from 'axios';
import { useSearchParams } from 'next/navigation';

// Define the type for your group data
interface GroupData {
  group_id: string;
  group_name: string;
  num_members: number;
  // Add more properties as needed
}

const GroupPage: React.FC = () => {
  const [group, setGroup] = useState<GroupData | null>(null);
  const [loading, setLoading] = useState(true);
  const searchParams = useSearchParams();

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
      <h1>Group ID: {group.group_id}</h1>
      <p>Group Name: {group.group_name}</p>
      <p>Members: {group.num_members}</p>
      {/* Add more details about the group as needed */}
    </div>
  );
};

export default GroupPage;
