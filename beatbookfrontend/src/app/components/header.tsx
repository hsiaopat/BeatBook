import React from 'react';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';

const Header: React.FC = () => {
  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6">BeatBook</Typography>
        {/* Add other header elements like buttons, icons, etc. */}
      </Toolbar>
    </AppBar>
  );
};

export default Header;
