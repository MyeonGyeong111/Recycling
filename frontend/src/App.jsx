import React, { useState, useEffect } from 'react';
import { UploadCloud, MessageSquare, Info, PackageOpen, Trash2, Search, Send, Image as ImageIcon } from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('helper'); // 'helper', 'guide', 'community'
  const [file, setFile] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  
  // Community state
  const [posts, setPosts] = useState([]);
  const [newTitle, setNewTitle] = useState('');
  const [newContent, setNewContent] = useState('');
  const [newAuthor, setNewAuthor] = useState('');
  const [newCategory, setNewCategory] = useState('GENERAL');

  // Categories for icons
  const CATEGORIES = [
    { id: 'PLASTIC', name: '플라스틱', icon: <PackageOpen size={40}/>, color: '#38bdf8' },
    { id: 'PAPER', name: '종이류', icon: <MessageSquare size={40}/>, color: '#fcd34d' },
    { id: 'GLASS', name: '유리병', icon: <Info size={40}/>, color: '#34d399' },
    { id: 'VINYL', name: '비닐류', icon: <Search size={40}/>, color: '#fb7185' },
    { id: 'CAN', name: '캔류', icon: <Trash2 size={40}/>, color: '#94a3b8' },
  ];

  const handleFileUpload = async (e) => {
    const f = e.target.files[0];
    if(!f) return;
    setFile(URL.createObjectURL(f));
    setLoading(true);
    
    // Call Predict API
    try {
      const formData = new FormData();
      formData.append('file', f);
      const res = await fetch('/api/v1/recycle/predict', { method: 'POST', body: formData });
      const data = await res.json();
      setPrediction(data);
    } catch(err) {
      console.error(err);
      setPrediction({category: "ERROR", message: "예측 서버에 연결할 수 없습니다."});
    }
    setLoading(false);
  };

  const loadPosts = async () => {
    try {
      const res = await fetch('/api/v1/community/posts');
      const data = await res.json();
      setPosts(data);
    } catch(err) {
      console.error("Failed to load posts", err);
    }
  };

  useEffect(() => {
    if(activeTab === 'community') loadPosts();
  }, [activeTab]);

  const submitPost = async (e) => {
    e.preventDefault();
    if(!newTitle || !newContent || !newAuthor) return;
    
    try {
      await fetch('/api/v1/community/posts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: newTitle, content: newContent, author: newAuthor, category: newCategory })
      });
      setNewTitle(''); setNewContent(''); setNewAuthor('');
      loadPosts();
    } catch(err) {
      console.error(err);
    }
  };

  const [selectedGuide, setSelectedGuide] = useState(null);
  const fetchGuideInfo = async (categoryId) => {
    try {
      const res = await fetch(`/api/v1/recycle/info/${categoryId}`);
      const data = await res.json();
      setSelectedGuide(data);
    } catch(err) { console.error(err); }
  }

  return (
    <div className="container">
      <h1 className="title">Recycling AI Assistant ♻️</h1>
      
      <div className="nav-tabs">
        <button className={`nav-tab ${activeTab === 'helper' ? 'active' : ''}`} onClick={() => setActiveTab('helper')}>
          <UploadCloud size={18} /> AI 분리수거 도우미
        </button>
        <button className={`nav-tab ${activeTab === 'guide' ? 'active' : ''}`} onClick={() => setActiveTab('guide')}>
          <Info size={18} /> 품목별 분리가이드
        </button>
        <button className={`nav-tab ${activeTab === 'community' ? 'active' : ''}`} onClick={() => setActiveTab('community')}>
          <MessageSquare size={18} /> 자취생 커뮤니티
        </button>
      </div>

      {activeTab === 'helper' && (
        <div className="glass-panel" style={{textAlign: 'center'}}>
          <h2>사진으로 분리수거 방법 찾기</h2>
          <p style={{color: '#94a3b8', marginBottom: '2rem'}}>헷갈리는 쓰레기, 스마트하게 사진으로 해결하세요!</p>
          
          <label className="file-input-wrapper">
            {file ? (
              <img src={file} alt="preview" style={{maxHeight:'200px', borderRadius:'12px', marginBottom: '1rem', border: '2px solid rgba(255,255,255,0.1)'}} />
            ) : (
              <ImageIcon size={60} color="#cbd5e1" style={{marginBottom:'1rem'}}/>
            )}
            <span style={{fontSize:'1.2rem', fontWeight:'bold', color: '#38bdf8'}}>사진 업로드 (클릭 또는 드래그)</span>
            <input type="file" accept="image/*" onChange={handleFileUpload} />
          </label>

          {loading && <p style={{marginTop: '2rem', color: '#38bdf8', fontWeight: 'bold'}}>✨ AI가 이미지를 꼼꼼히 분석중입니다...</p>}
          
          {prediction && !loading && (
            <div className="prediction-result glass-panel" style={{marginTop: '2rem', background: 'rgba(56, 189, 248, 0.05)', borderColor: '#38bdf8'}}>
              <h3 style={{color: '#38bdf8', fontSize: '1.5rem', marginBottom: '8px'}}>인식 결과: {prediction.category}</h3>
              <p style={{fontSize: '1.1rem', marginBottom: '12px'}}>{prediction.message}</p>
              {prediction.confidence && <span className="badge">정확도: {(prediction.confidence * 100).toFixed(1)}%</span>}
            </div>
          )}
        </div>
      )}

      {activeTab === 'guide' && (
        <div className="glass-panel">
          <h2 style={{textAlign:'center', marginBottom:'1rem'}}>분리수거 대표 카테고리 살펴보기</h2>
          <p style={{textAlign:'center', color: '#94a3b8', marginBottom:'2rem'}}>궁금한 항목의 아이콘을 선택하세요.</p>
          
          <div className="grid">
            {CATEGORIES.map(cat => (
              <div 
                key={cat.id} 
                className="category-card glass-panel" 
                onClick={() => fetchGuideInfo(cat.id)}
                style={{borderColor: selectedGuide?.category === cat.id ? '#38bdf8' : 'rgba(255,255,255,0.1)'}}
              >
                <div style={{color: cat.color}}>{cat.icon}</div>
                <h3 style={{margin:0}}>{cat.name}</h3>
              </div>
            ))}
          </div>

          {selectedGuide && (
            <div className="glass-panel" style={{marginTop: '2rem', borderLeft: '4px solid #38bdf8', background: 'rgba(0,0,0,0.2)'}}>
              <h3 style={{color: '#38bdf8', fontSize: '1.25rem'}}>{selectedGuide.description}</h3>
              <p style={{fontSize: '1.1rem', lineHeight: 1.6}}>{selectedGuide.how_to_recycle}</p>
            </div>
          )}
        </div>
      )}

      {activeTab === 'community' && (
        <div className="glass-panel">
          <h2>자취생 고충 나눔터</h2>
          <p style={{color: '#94a3b8', marginBottom: '2rem'}}>서로의 분리수거 꿀팁이나 헷갈리는 점들을 자유롭게 물어보세요!</p>
          
          <form className="glass-panel" onSubmit={submitPost} style={{marginBottom: '2rem', background: 'rgba(0,0,0,0.2)'}}>
            <h3>새 이야기 남기기</h3>
            <div style={{display:'flex', gap:'12px', flexWrap: 'wrap'}}>
              <input className="input-field" style={{flex: 1, minWidth: '150px'}} placeholder="닉네임 (익명가능)" value={newAuthor} onChange={e=>setNewAuthor(e.target.value)} required />
              <select className="input-field" style={{flex: 1, minWidth: '150px'}} value={newCategory} onChange={e=>setNewCategory(e.target.value)}>
                <option value="GENERAL">일반/기타</option>
                {CATEGORIES.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
              </select>
            </div>
            <input className="input-field" placeholder="제목을 입력해주세요." value={newTitle} onChange={e=>setNewTitle(e.target.value)} required />
            <textarea className="input-field" placeholder="자세한 내용을 들려주세요..." value={newContent} onChange={e=>setNewContent(e.target.value)} required />
            <button type="submit" className="btn" style={{width: '100%', fontSize: '1.1rem'}}><Send size={18}/> 작성 완료</button>
          </form>

          <div className="post-list">
            <h3 style={{marginBottom: '1rem'}}>최신 게시글</h3>
            {posts.map(post => (
              <div key={post.id} className="post-card">
                <div className="post-header">
                  <h3 className="post-title">{post.title}</h3>
                  <span className="badge">{post.category}</span>
                </div>
                <p className="post-content">{post.content}</p>
                <div style={{color: '#64748b', fontSize: '0.9rem', marginTop:'16px', display:'flex', justifyContent: 'space-between'}}>
                  <span>작성자: {post.author}</span>
                  <span>{new Date(post.created_at).toLocaleString()}</span>
                </div>
              </div>
            ))}
            {posts.length === 0 && <p style={{textAlign:'center', color:'#64748b', margin: '3rem 0'}}>아직 등록된 이야기가 없습니다. 첫 글을 작성해보세요!</p>}
          </div>
        </div>
      )}
    </div>
  );
}
