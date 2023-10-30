// src/App.tsx

import React from 'react';
import Home from './pages/index'

const App: React.FC = () => {
  const username = 'John'; // Replace with the actual username or fetch it from an API

  return (
    <div>
      <header>
        <h1>React TypeScript App</h1>
      </header>
      <main>
        <Home username={username} />
      </main>
    </div>
  );
};

export default App;
