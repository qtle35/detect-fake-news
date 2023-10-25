import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './components/home';
import CustomSidebar from './components/sidebar';
import LabelPage from './components/label-page';
import React from 'react';
import LabelEdit from './components/label-edit';
import Login from './components/login';
import { AuthProvider } from './components/auth-context'

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <div className='grid grid-cols-6'>
          <div className='col-span-1'>
            <CustomSidebar />
          </div>
          <div className='col-span-5'>
            <main>
              <Routes>
                {/* <Route path="/home" element={<Home />} /> */}
                <Route path='/' element={<Home />} />
                <Route path='/login' element={<Login />} />
                <Route path='/label' element={<LabelPage />} />
                <Route path='/label/:id' element={<LabelEdit />} />
              </Routes>
            </main>
          </div>

        </div>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
