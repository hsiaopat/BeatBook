/* import Link from 'next/link';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import { styled } from '@mui/system'

const containerStyles = {
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'flex-start',
  alignItems: 'center',
  height: '100vh',
};

const whiteBackgroundStyles = {
  background: 'white',
  width: '100%',
  borderBottom: '1px solid black',
};

const titleStyles = {
  fontSize: '2rem',
  color: 'black',
  margin: 0,
  textAlign: 'center',
  padding: '1rem 0',
};

const centeredButtonStyles = {
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'center',
  alignItems: 'center',
  flex: 1,
};

const greenButtonStyles = {
  backgroundColor: 'forestgreen', // Set the background color to green
  color: 'black', // Set the text color to black
  fontSize: '1rem',
  margin: '1rem 0',
  '&:hover': {
    backgroundColor: 'forestgreen', // Set the background color to green on hover
  },
};

const HomePage = () => {
  return (
    <Box sx={containerStyles}>
      <Box sx={whiteBackgroundStyles}>
        <Box sx={titleStyles}>BeatBook</Box>
      </Box>
      <Box sx={centeredButtonStyles}>
        <Link href="/group-login">
          <Button sx={greenButtonStyles} variant="contained">
            Group Login
          </Button>
        </Link>
      </Box>
    </Box>
  );
};

export default HomePage;

*/


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
        <Link href="/group-login">
          <GreenButton variant="contained">Group Login</GreenButton>
        </Link>
      </CenteredButton>
    </Container>
  );
};

export default HomePage;