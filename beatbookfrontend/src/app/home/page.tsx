'use client'
import Link from 'next/link';
import Button from '@mui/material/Button';
import { styled } from '@mui/system';

const Container = styled('div')({
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'flex-start',
  alignItems: 'center',
  height: '100vh',
});

const WhiteBackground = styled('div')({
  background: 'white',
  width: '100%',
  borderBottom: '1px solid black',
});

const Title = styled('h1')({
  fontSize: '2rem',
  color: 'black',
  margin: 0,
  textAlign: 'center',
  padding: '1rem 0',
});

const CenteredButtons = styled('div')({
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'center',
  alignItems: 'center',
  flex: 1,
});

const GreenButton = styled(Button)({
  backgroundColor: 'forestgreen',
  color: 'black',
  fontSize: '1rem',
  margin: '1rem 0',
});

const SpotifyLoginButton = styled(Button)({
  backgroundColor: 'lightblue', // Customize the background color for the Spotify login button
  color: 'black', // Text color
  fontSize: '1rem',
  margin: '1rem 0',
});

const HomePage = () => {
  const redirectToSpotify = () => {
    // Save the user ID or perform any other necessary actions
    const userId = 'your-user-id'; // Replace with actual user ID
    // Redirect to the Spotify login page
    window.location.href = 'https://accounts.spotify.com';
  };

  return (
    <Container>
      <WhiteBackground>
        <Title>BeatBook</Title>
      </WhiteBackground>
      <CenteredButtons>
        <SpotifyLoginButton variant="contained" onClick={redirectToSpotify}>
          Log in to Spotify
        </SpotifyLoginButton>
        <Link href="/group-login">
          <GreenButton variant="contained">Group Login</GreenButton>
        </Link>
      </CenteredButtons>
    </Container>
  );
};

export default HomePage;

/* 'use client'
import Link from 'next/link';
import Button from '@mui/material/Button';
import { styled } from '@mui/system';


const Container = styled('div')({
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'flex-start',
  alignItems: 'center',
  height: '100vh',
});

const WhiteBackground = styled('div')({
  background: 'white', // Set white background color
  width: '100%',
  borderBottom: '1px solid black', // Add a black border at the bottom to create the black line
});

const Title = styled('h1')({
  fontSize: '2rem',
  color: 'black',
  margin: 0,
  textAlign: 'center',
  padding: '1rem 0', // Add padding for spacing
});

const CenteredButton = styled('div')({
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'center',
  alignItems: 'center',
  flex: 1,
});

const GreenButton = styled(Button)({
  backgroundColor: 'forestgreen',
  color: 'black',
  fontSize: '1rem',
  margin: '1rem 0',
});

const HomePage = () => {
  return (
    <Container>
      <WhiteBackground>
        <Title>BeatBook</Title>
      </WhiteBackground>
      <CenteredButton>
        <Link href="">
          <GreenButton variant="contained">Group Login</GreenButton>
        </Link>
      </CenteredButton>
    </Container>
  );
};

export default HomePage;

*/
