import * as React from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Link from '@mui/material/Link';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import {get,post} from '../utils/requests'
import {root} from '../index.js';
import {appName} from '../js/Globals.js';
import './../css/guestUI.css';


/* Copyright label */
function Copyright(props) {
  const navigate = useNavigate();
  return (
    <Typography variant="body2" color="text.secondary" align="center" {...props}>
      {'Copyright © '}
      <Link color="inherit" onClick={() => navigate('/contact', false)}>
        {appName}
      </Link>{' '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}

const theme = createTheme();

export default function GuestUI() {
  const navigate = useNavigate();

  /* Handle eventID button click */
  const handleSubmit = (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const eventID = data.get('eventID');


    // Proceed if all the fields are entered. Otherwise, display an alert to the user
    if (eventID !== 0) {

      const requests_data = {
        'eventID': eventID,
      }
/* this code from signup will be useful I assume */
      post('api/user/register/', requests_data) // POST data to webserver
        .then(function (res) {

          console.log("Response: " + res);

          // If the response code is 200, signup is successful. Proceed to SignIn page. Otherwise, display an alert to the user
          if (res.status === 200) {
            navigate("/signin", false)
          } else {
            alert("Sign Up failed, please try again !");
          }
        })
        .catch(function (res) {
          console.log("Error : " + res)
          alert("Wrong ID, please try again !");

        })

    } else {
      alert("Please fill all the fields !");
    }
  };

  document.body.style.backgroundColor = "rgb(41, 118, 219)";

  return (
    <ThemeProvider theme={theme}>
      <Container component="main" maxWidth="sm">
        <CssBaseline />
        <Box className="guestbox">
          <Typography component="h1" variant="h5">
            Enter Event ID:
          </Typography>
          <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
          <Grid container spacing={2}>
  <Grid item xs={12}>
    <TextField
      name="eventID"
      required
      label="Event ID"
      autoFocus
      fullWidth
    />
  </Grid>
  <Grid item xs={12}>
    <Button
      type="submit"
      fullWidth
      variant="contained"
      sx={{ mt: 3, mb: 2 }}
    >
      Submit
    </Button>
  </Grid>
</Grid>
          </Box>
        </Box>
        <Copyright sx={{ mt: 5 }} />
      </Container>
    </ThemeProvider>
  );
}