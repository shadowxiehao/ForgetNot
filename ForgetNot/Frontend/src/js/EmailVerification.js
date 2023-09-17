import React, { useState, useEffect } from 'react';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import {post} from '../utils/requests'

const EmailVerification = ({email,onCodeChange}) => {
    const [buttonDisabled, setButtonDisabled] = useState(false);
    const [timeRemaining, setTimeRemaining] = useState(0);
    const [code, setCode] = useState(null); // state to store the verification code

    let timer;

    const handleSubmit = () => {
        console.log(email)
        if (!email) {
            alert('Please enter your email address first');
            return;
        }

        // Use the email prop as needed, for example, to send the verification code
        console.log('Sending verification code to:', email);

        post('/api/user/generate_verification_code/',{email:email})
            .then(function (res){console.log(res)})

        setButtonDisabled(true);
        setTimeRemaining(60);

        // Handle form submission logic here, e.g., send the verification code to the user


        // Start the countdown
        timer = setInterval(() => {
            setTimeRemaining((prevTime) => prevTime - 1);
        }, 1000);

        // Disable the button for 60 seconds
        setTimeout(() => {
            setButtonDisabled(false);
            clearInterval(timer);
        }, 60 * 1000);
    };

    useEffect(() => {
        return () => {
            clearInterval(timer);
        };
    }, []);

    const handleClick = (e) => {
        e.preventDefault(); // Prevent form submission
        handleSubmit();
    };

    return (
        <Box
            sx={{
                display: 'flex',
                flexDirection: 'row',
                alignItems: 'center',
                justifyContent: 'center',
                gap: 2,
                width: '100%',
                maxWidth: '100%', // Add this line to set the max width to 100%
            }}
			fullWidth
        >
            <TextField
                label="6-Digit Verification Code"
                variant="outlined"
                value={code}
                onChange={(e) => onCodeChange(e.target.value)}
                inputProps={{ maxLength: 6 }}
                required
				fullWidth
            />
            <Button fullWidth type="submit" variant="contained" color="primary" disabled={buttonDisabled} style={{textTransform: 'none'}}
                    onClick={handleClick} // Use handleClick instead of handleSubmit
            >
                {buttonDisabled ? `${timeRemaining} s` : 'Send Verification Code'}
            </Button>
        </Box>
    );
};

export default EmailVerification;
