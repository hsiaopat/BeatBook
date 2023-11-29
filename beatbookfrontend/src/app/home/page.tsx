'use client'
import Link from 'next/link';
import Button from '@mui/material/Button';
import { styled } from '@mui/system';
import axios from 'axios';

const Container = styled('div')({
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'flex-start',
  alignItems: 'center',
  height: '100vh',
}); 

const HeaderBackground = styled('div')({
  background: 'darkseagreen',
  width: '100%',
  borderBottom: '1px solid black',
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
  padding: '1rem',
});

const Title = styled('h1')({
  fontSize: '2rem',
  color: 'black',
  margin: 0,
  textAlign: 'center',
  marginLeft: '44.5%'
});

const CenteredButtons = styled('div')({
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  flex: 1,
});

const GreenButton = styled(Button)({
  backgroundColor: 'darkseagreen',
  color: 'black',
  fontSize: '1.2rem', // Slightly larger font size
  padding: '1rem 2rem', // Increase button padding for larger size
  margin: '1rem 0',
});

const TopGreenButton = styled(Button)({
  backgroundColor: 'darkseagreen',
  color: 'black',
  fontSize: '1.2rem', // Slightly larger font size
  padding: '1rem 2rem', // Increase button padding for larger size
  margin: '1rem 0',
});

const WelcomeMessage = styled('div')({
  backgroundColor: 'white', // Change the background color to pale green
  border: '1px solid black',
  padding: '1rem',
  textAlign: 'center',
  width: '65%',
  marginTop: '1rem', // Move closer to the black line
});


const SpotifyLoginButton = styled(Button)({
  backgroundColor: 'white',
  color: 'black',
  fontSize: '1rem',
  marginRight: '1rem',
  marginBottom: '1rem',
});



const HomePage = () => {
  const redirectToSpotify = async () => {
    try {
      const spotifyAuthUrl = 'http://129.74.153.235:5028/login';
      window.location.href = spotifyAuthUrl;
    } catch (error) {
      console.error('Error initiating Spotify login:', error);
    }
  };
  

  return (
    <div>
      <HeaderBackground>
        <Title>BeatBook</Title>
        <SpotifyLoginButton variant="contained" onClick={redirectToSpotify}>
          Spotify Login
        </SpotifyLoginButton>
      </HeaderBackground>
      

      

      <nav className="bg-white border-gray-200 dark:bg-gray-900">
          <div className="flex flex-wrap justify-between items-center mx-auto max-w-screen-xl p-4">
              <a href="https://flowbite.com" className="flex items-center space-x-3 rtl:space-x-reverse">
                  <img src="https://flowbite.com/docs/images/logo.svg" className="h-8" alt="Flowbite Logo" />
                  <span className="self-center text-2xl font-semibold whitespace-nowrap dark:text-white">Flowbite</span>
              </a>
              <div className="flex items-center space-x-6 rtl:space-x-reverse">
                  <a href="tel:5541251234" className="text-sm  text-gray-500 dark:text-white hover:underline">(555) 412-1234</a>
                  <a href="#" className="text-sm  text-blue-600 dark:text-blue-500 hover:underline">Login</a>
              </div>
          </div>
      </nav>
      <nav className="bg-gray-50 dark:bg-gray-700">
          <div className="max-w-screen-xl px-4 py-3 mx-auto">
              <div className="flex items-center">
                  <ul className="flex flex-row font-medium mt-0 space-x-8 rtl:space-x-reverse text-sm">
                      <li>
                          <a href="#" className="text-gray-900 dark:text-white hover:underline" aria-current="page">Home</a>
                      </li>
                      <li>
                          <a href="#" className="text-gray-900 dark:text-white hover:underline">Company</a>
                      </li>
                      <li>
                          <a href="#" className="text-gray-900 dark:text-white hover:underline">Team</a>
                      </li>
                      <li>
                          <a href="#" className="text-gray-900 dark:text-white hover:underline">Features</a>
                      </li>
                  </ul>
              </div>
          </div>
      </nav>


      <CenteredButtons>
      <WelcomeMessage>
          Welcome to BeatBook, a “book club” for music albums. 
          Login to your Spotify account and join a group of other users.
          From your personal music listening statistics, the “club” will 
          recommend an album to listen to that week that you can then rank and make comments about.
           The groups ranking of that weeks album can then help determine future albums to recommend to you. HELP CLAIRE!!!
      </WelcomeMessage>
      <Link href="/topartists">
      <TopGreenButton variant="contained">
          Display Top Artists
        </TopGreenButton>
      </Link>
      <Link href="/toptracks">
        <TopGreenButton variant="contained">
          Display Top Tracks
        </TopGreenButton>
        </Link>
        <Link href="/groups">
          <GreenButton variant="contained">Join Group</GreenButton>
        </Link>
      </CenteredButtons>
    </div>
  );
};

export default HomePage;