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
      
      

      <nav className="bg-white border-gray-200 dark:bg-gray-900">
          <div className="flex flex-wrap justify-between items-center mx-auto max-w-screen-xl p-4">
            <a href="https://spotify.com" className="flex items-center space-x-3 rtl:space-x-reverse">
              <span className="self-center text-2xl font-semibold whitespace-nowrap dark:text-white">BeatBook</span>
            </a>
            <div className="flex items-center space-x-6 rtl:space-x-reverse">
              <a href="#" className="text-sm text-blue-600 dark:text-blue-500 hover:underline" onClick={redirectToSpotify}>Login</a>
            </div>
          </div>
        </nav>
      


      <CenteredButtons className="mb-8">
      <div className="sm:flex items-center max-w-screen-xl">
        <div className="sm:w-1/2 p-10">
          <div className="image object-center text-center">
            <img src="https://i.imgur.com/WbQnbas.png" />
          </div>
        </div>
        <div className="sm:w-1/2 p-5">
          <div className="text">
            <span className="text-gray-500 border-b-2 border-blue-600 uppercase">About us</span>
            <h2 className="my-4 font-bold text-3xl  sm:text-4xl ">About <span className="text-blue-600">BeatBook</span>
            </h2>
            <p className="text-gray-700">
            Welcome to BeatBook, a “book club” for music albums. 
            Login to your Spotify account and join a group of other users.
            From your personal music listening statistics, the “club” will 
            recommend an album to listen to that week that you can then rank and make comments about.
            The groups ranking of that weeks album can then help determine future albums to recommend to you. HELP CLAIRE!!!
            </p>
          </div>
        </div>
      </div>
      <div className="flex justify-between items-center">
      {/* Container 1 */}
      <Link href="/topartists">
        <a>
          <div className="flex flex-col items-center border border-gray-300 p-4 rounded-md hover:shadow-lg transition-transform duration-300 transform hover:scale-105 cursor-pointer w-64 h-48">
            <div className="bg-blue-600 text-white p-4 rounded-md">
              Display Top Artists
            </div>
            <p className="text-gray-600 mt-2">Explore your top artists.</p>
          </div>
        </a>
      </Link>

      {/* Container 2 */}
      <Link href="/toptracks">
        <a>
          <div className="flex flex-col items-center border border-gray-300 p-4 rounded-md hover:shadow-lg transition-transform duration-300 transform hover:scale-105 cursor-pointer w-64 h-48 ml-4">
            <div className="bg-blue-600 text-white p-4 rounded-md">
              Display Top Tracks
            </div>
            <p className="text-gray-600 mt-2">Discover your top tracks.</p>
          </div>
        </a>
      </Link>

      {/* Container 3 */}
      <Link href="/gallery">
        <a>
          <div className="flex flex-col items-center border border-gray-300 p-4 rounded-md hover:shadow-lg transition-transform duration-300 transform hover:scale-105 cursor-pointer w-64 h-48 ml-4">
            <div className="bg-blue-600 text-white p-4 rounded-md">
              Display BeatGroups
            </div>
            <p className="text-gray-600 mt-2">Connect with like-minded music enthusiasts.</p>
          </div>
        </a>
      </Link>
    </div>
      </CenteredButtons>
    <br></br>
    </div>
  );
};

export default HomePage;