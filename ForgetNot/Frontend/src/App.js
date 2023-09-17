import './App.css';
import { Routes, Route } from 'react-router-dom';
import { BrowserRouter } from 'react-router-dom';


import Home from './js/Home.js';
import SignIn from './js/SignIn.js';
import SignUp from './js/SignUp.js';
import Landing from './js/Landing.js';
import Contact from './js/Contact.js';
import Profile from './js/Profile.js';
import Guest from './js/Guest.js';


const App = () => {
 return (
    <>
	  <BrowserRouter>

       <Routes>
	      <Route path="/" element={<Landing />} />

		  <Route path="/signup" element={<SignUp />} />
          <Route path="/signin" element={<SignIn />} />
          <Route path="/home" element={<Home />} />
	<Route path="/contact" element={<Contact />} />
	<Route path="/profile" element={<Profile />} />
	<Route path="/guest" element={<Guest />} />
       </Routes>
	     </BrowserRouter>


    </>
 );
};

export default App;


