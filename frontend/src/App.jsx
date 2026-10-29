import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Home from './pages/Home';
import YoutubeSummarizer from './pages/YoutubeSummarizer';
import DocumentSummarizer from './pages/DocumentSummarizer';
import WebsiteSummarizer from './pages/WebsiteSummarizer';
import TextSummarizer from './pages/TextSummarizer';
import { useTheme } from './hooks/useTheme';

function AppShell() {
  // Initialize theme system at the app root
  useTheme();

  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/"           element={<Home />} />
        <Route path="/youtube"    element={<YoutubeSummarizer />} />
        <Route path="/documents"  element={<DocumentSummarizer />} />
        <Route path="/website"    element={<WebsiteSummarizer />} />
        <Route path="/text"       element={<TextSummarizer />} />
        {/* Catch-all redirect */}
        <Route path="*"           element={<Navigate to="/" replace />} />
      </Routes>
      <Footer />
    </BrowserRouter>
  );
}

export default function App() {
  return <AppShell />;
}
