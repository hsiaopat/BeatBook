'use client'
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Dialog, Transition } from '@headlessui/react';
import '../globals.css';
import { styled } from '@mui/system';
import Link from 'next/link';


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

interface Group {
 group_id: string;
 group_name: string;
 num_members: number;
}


const GroupsGallery: React.FC = () => {
  const [groups, setGroups] = useState<Group[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [createGroupModalOpen, setCreateGroupModalOpen] = useState(false);
  const [newGroupName, setNewGroupName] = useState('');


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
  

  const handleCreateGroup = async () => {
    try {
      // Make the POST request with the newGroupName parameter
      const response = await axios.post('http://129.74.153.235:5028/creategroup', { group_name: newGroupName });
      console.log(response.data);
      // add code to update UI or perform additional actions after creating
      // For example, you might want to clear the input field and close the modal
      setNewGroupName('');
      setCreateGroupModalOpen(false);
      window.location.href = 'http://129.74.153.235:5029/gallery'
    } catch (error) {
      console.error(error);
    }
  };
  


  useEffect(() => {

    const handleCreateGroupClient = () => {
      handleCreateGroup();
    };
    document.getElementById('createGroupButton')?.addEventListener('click', handleCreateGroupClient);
    handleDisplayGroups();

    return () => {
      document.getElementById('createGroupButton')?.removeEventListener('click', handleCreateGroupClient);
    };
  }, []); // Empty dependency array ensures the effect runs only once on mount


 const handleSearch = () => {
   // Perform search logic based on the entered group name
   const filteredGroups = groups.filter(group => group.group_name.includes(searchTerm));
   setGroups(filteredGroups);
 };




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
             <a href="/home" className="flex items-center space-x-3 rtl:space-x-reverse">
               <span className="self-center text-2xl font-semibold whitespace-nowrap dark:text-white">BeatBook</span>
             </a>
             <div className="flex items-center space-x-6 rtl:space-x-reverse">
               <a href="#" className="text-sm text-blue-600 dark:text-blue-500 hover:underline" onClick={redirectToSpotify}>Login</a>
             </div>
           </div>
         </nav>

         <div className="container mx-auto my-8 text-center">
          <Title>Group Gallery</Title>


        <div className="flex items-center justify-center mb-4">
          <input
            type="text"
            className="p-2 border border-gray-300 rounded-l focus:outline-none"
            placeholder="Enter group name"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          <button
            className="bg-grey text-black p-2 rounded-r hover:bg-blue-600 focus:outline-none"
            onClick={handleSearch}
          >
            Search Groups
          </button>
        </div>
        <div className="flex items-center justify-center mb-4">
        <button
          className="block mx-auto bg-blue-600 text-white p-2 rounded hover:bg-green-600 focus:outline-none"
          onClick={() => setCreateGroupModalOpen(true)}
        >
          Create Group
        </button>
</div>

<div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 mt-4">
  {groups.map((group) => (
    // Check if num_members is greater than 0 before rendering
    group.num_members > 0 && (
      <Link key={group.group_id} href={`/group?group_id=${group.group_id}`}>
        <a>
          <div className="bg-white p-4 border border-gray-300 rounded cursor-pointer hover:shadow-lg transition-transform duration-300 transform hover:scale-105">
            <p className="text-lg font-bold">{`${group.group_name} - Members: ${group.num_members}`}</p>
          </div>
        </a>
      </Link>
    )
  ))}
</div>
     </div>


     {/* Create Group Modal */}
     <Transition show={createGroupModalOpen} as={React.Fragment}>
       <Dialog
         as="div"
         className="flex items-center justify-center"
         onClose={() => setCreateGroupModalOpen(false)}
       >
         <div className="min-h-screen px-4 text-center">
           <Transition.Child
             as={React.Fragment}
             enter="ease-out duration-300"
             enterFrom="opacity-0"
             enterTo="opacity-100"
             leave="ease-in duration-200"
             leaveFrom="opacity-100"
             leaveTo="opacity-0"
           >
             <Dialog.Overlay className="fixed inset-0 bg-black opacity-30" />
           </Transition.Child>


           <span className="inline-block h-screen align-middle" aria-hidden="true">
             &#8203;
           </span>


           <Transition.Child
             as={React.Fragment}
             enter="ease-out duration-300"
             enterFrom="opacity-0 scale-95"
             enterTo="opacity-100 scale-100"
             leave="ease-in duration-200"
             leaveFrom="opacity-100 scale-100"
             leaveTo="opacity-0 scale-95"
           >
             <div className="inline-block w-full max-w-md p-6 my-8 overflow-hidden transition-all transform bg-white shadow-md rounded mx-auto">
               <Dialog.Title as="h3" className="text-lg font-medium leading-6 text-gray-900">
                 Create a New Group
               </Dialog.Title>
               <div className="mt-2">
                     <label htmlFor="groupName" className="block text-sm font-medium text-gray-700">
                       Group Name
                     </label>
                     <p></p>
                     <input
                       type="text"
                       id="groupName"
                       name="groupName"
                       className="mt-1 p-2 border border-gray-300 rounded w-full"
                       value={newGroupName}
                       onChange={(e) => setNewGroupName(e.target.value)}
                     />
                   </div>
  
                   <div className="mt-4">
                   <button id="createGroupButton"
                   type="button"
                   className="ml-2 inline-flex justify-center px-4 py-2 text-sm font-medium text-gray-700 bg-gray-200 border border-transparent rounded-md hover:bg-gray-300 focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-blue-500"
                   onClick={() => handleCreateGroup()}
                 >
                   Create Group
                  </button>
                 <button
                   type="button"
                   className="ml-2 inline-flex justify-center px-4 py-2 text-sm font-medium text-gray-700 bg-gray-200 border border-transparent rounded-md hover:bg-gray-300 focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-blue-500"
                   onClick={() => setCreateGroupModalOpen(false)}
                 >
                   Cancel
                     </button>
                   </div>
                 </div>
               </Transition.Child>
             </div>
           </Dialog>
         </Transition>
  
       </>
     );
   };
  
   export default GroupsGallery;

