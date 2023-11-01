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
  margin: '10rem 0',
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
  const redirectToSpotify = () => {
    // Save the user ID or perform any other necessary actions
    const userId = 'your-user-id'; // Replace with the actual user ID
    // Redirect to the Spotify login page
    window.location.href = 'https://accounts.spotify.com';
  };

  return (
    <Container>
      <HeaderBackground>
        <Title>BeatBook</Title>
        <SpotifyLoginButton variant="contained" onClick={redirectToSpotify}>
          Spotify Login
        </SpotifyLoginButton>
      </HeaderBackground>
      <CenteredButtons>
      <WelcomeMessage>
          Welcome to BeatBook, a “book club” for music albums. 
          Login to your Spotify account and join a group of other users.
          From your personal music listening statistics, the “club” will 
          recommend an album to listen to that week that you can then rank and make comments about.
           The groups ranking of that weeks album can then help determine future albums to recommend to you.
      </WelcomeMessage>
        <Link href="/group-login">
          <GreenButton variant="contained">Join Group</GreenButton>
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
