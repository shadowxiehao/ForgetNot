import * as React from 'react';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Link from '@mui/material/Link';
import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { useNavigate } from 'react-router-dom';
import axios from "axios";

import {get,post} from '../utils/requests';
import '../css/contact.css';

var publicPath=process.env.PUBLIC_URL;
var logoPath= 'assets/images/background.jpg';

const theme = createTheme();

function ContactUsPage() {
  const navigate = useNavigate();
  
  /* Handle send button click */

  const handleSubmit = (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
	const userName = data.get('userName');
	const userEmail = data.get('userEmail');
	const userMessage = data.get('userMessage');
	
    console.log({
	  userName: userName,
	  userEmail: userEmail,
      userMessage: userMessage     
	  
    });
	
	

	  // Proceed if all the fields are entered. Otherwise, display an alert to the user */
	  if(userName.length!==0 && userEmail.length!==0 && userMessage.length!==0)
		{
				
			const requests_data = {
				  'name':userName,
				  'email':userEmail,
				  'message':userMessage,
				 
			  }
			  
			  post('/api/general/contact/', requests_data) // POST data to webserver
				  .then(function (res){
					 
					console.log("Response: "+res);

					// If the response code is 200, signup is successful. Proceed to SignIn page. Otherwise, display an alert to the user
					  if(res.status === 200){
						  alert("Message sent, we will be in touch with you shortly !");
					  }else{
						  alert("Message sending failed, please try again !");
					  }
				  })
				  .catch(function (res){
					  console.log("Error : "+res)
					  alert("Message sending failed, please try again !");

				  })
			
		}else{
			alert("Please fill all the fields !");
		}
  

  };


  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{
        height: '100vh',
        backgroundImage: `url(${publicPath+logoPath})`,
        backgroundRepeat: 'no-repeat',
        backgroundPosition: 'center',
        backgroundSize: 'cover',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        flexDirection: 'column',
        px: 4,
      }}>
        <Box >
          <Typography component="h2" variant="h2" fontFamily="Baskerville" className="contacttitle">
            Contact Us
          </Typography>

          <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 4 }}>
            <TextField
              required
              id="userName"
              label="Name"
			  name="userName"
              variant="outlined"
              margin="normal"
              fullWidth
              className="text"

            />
            <TextField
              required
              id="userEmail"
              label="Email"
			  name="userEmail"
              variant="outlined"
              margin="normal"
              fullWidth
              className="text"
            />
            <TextField
              required
              id="userMessage"
              label="Message"
			  name="userMessage"
              variant="outlined"
              margin="normal"
              multiline
              rows={4}
              fullWidth
              className="text"
            />
            <Button
              variant="contained"
			  type="submit"
              className="button"
            >
              Send
            </Button>
          </Box>

          <Typography component="p" variant="body1" align="center" fontFamily="Baskerville" >
            <Link className="contactlink" onClick={() => navigate('/', false)}>Back to Home</Link>
          </Typography>
        </Box>
      </Box>
    </ThemeProvider>
  );
}

export default ContactUsPage;


