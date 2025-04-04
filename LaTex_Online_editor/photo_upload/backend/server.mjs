import express from 'express';
import multer from 'multer';
import cors from 'cors';
import path from 'path';
import fs from 'fs';
import archiver from 'archiver';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = 4000;

// Enable CORS
app.use(cors());

// Set up directories
const UPLOAD_DIR = path.join(__dirname, 'uploads');
if (!fs.existsSync(UPLOAD_DIR)) {
    fs.mkdirSync(UPLOAD_DIR);
}

const ZIPPED_TEX_DIR = path.join(__dirname, 'zipped_tex');
if (!fs.existsSync(ZIPPED_TEX_DIR)) {
    fs.mkdirSync(ZIPPED_TEX_DIR);
}

// Configure Multer for file uploads
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, UPLOAD_DIR);
    },
    filename: (req, file, cb) => {
        cb(null, `${Date.now()}-${file.originalname}`);
    },
});
const upload = multer({ storage });

// Define routes
app.get('/', (req, res) => {
    res.send('Welcome to the Photo Upload Backend!');
});

app.post('/upload', upload.single('photo'), (req, res) => {
    if (!req.file) {
        return res.status(400).json({ error: 'No file uploaded' });
    }

    const uploadedPhotoPath = req.file.path;
    const uploadedPhotoName = req.file.originalname;

    const zipFileName = `${path.basename(uploadedPhotoName, path.extname(uploadedPhotoName))}.zip`;
    const zipFilePath = path.join(ZIPPED_TEX_DIR, zipFileName);

    const output = fs.createWriteStream(zipFilePath);
    const archive = archiver('zip', { zlib: { level: 9 } });

    output.on('close', () => {
        res.json({
            message: 'File uploaded and .zip file created successfully',
            photo_path: `/uploads/${req.file.filename}`,
            zip_file_path: `/zipped_tex/${zipFileName}`,
        });
    });

    archive.on('error', (err) => {
        res.status(500).json({ error: 'Error creating zip file' });
    });

    archive.pipe(output);

    const mainTexPath = path.join(__dirname, 'main.tex');
    if (fs.existsSync(mainTexPath)) {
        archive.file(mainTexPath, { name: 'main.tex' });
    } else {
        return res.status(500).json({ error: 'main.tex file not found' });
    }

    archive.finalize();
});

// Serve static files
app.use('/uploads', express.static(UPLOAD_DIR));
app.use('/zipped_tex', express.static(ZIPPED_TEX_DIR));

// Start the server only if this file is executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
    app.listen(PORT, () => {
        console.log(`Server is running at http://127.0.0.1:${PORT}`);
    });
}

export default app;