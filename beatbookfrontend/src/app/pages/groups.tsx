import React from 'react';
import Button from '@mui/material/Button';
import axios from 'axios';

const GroupsPage: React.FC = () => {
    const handleJoinGroup = async () => {
        try {
            const response = await axios.post('/join-group',{userId: 'yourUserId',groupId:'groupIdToJoin'});
            console.log(response.data);
            // add code to update UI or perform additional actions after joining
        } catch (error){
            console.error(error);
        }
    };

    const handleLeaveGroup = async () => {
        try {
            const response = await axios.post('/leave-group',{userId: 'yourUserId',groupId:'groupIdToJoin'});
            console.log(response.data);
            // add code to update UI or perform additional actions after leaving
        } catch (error){
            console.error(error);
        }
    };

    return (
        <div className="bg-black min-h-screen flex flex-col items-center justify-center text-white">
            <h1 className="text-4x1 font-bold mb-4">Beatbook Groups</h1>
            <div className="space-x-4">
                <Button 
                    variant="contained"
                    color="primary"
                    onClick={handleJoinGroup}
                >Join Group</Button>

<Button 
                    variant="contained"
                    color="secondary"
                    onClick={handleLeaveGroup}
                >Leave Group</Button>
            </div>
        </div>
    );
};

export default GroupsPage;