
// pages/index.tsx
//page for home screen
// src/pages/Home.tsx

import React from 'react';

interface HomeProps {
  username: string;
}

const Home: React.FC<HomeProps> = ({ username }) => {
  return (
    <div>
      <h1>Welcome to the Home Page, {username}!</h1>
      <p>This is a sample home page built with React and TypeScript.</p>
    </div>
  );
};

export default Home;
