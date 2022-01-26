import * as React from 'react';
import {useEffect, useState} from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';

import {initializeApp} from 'firebase/app';
import {getDatabase, onValue, ref} from 'firebase/database';

const firebaseConfig = {
    apiKey: process.env.REACT_APP_apiKey,
    authDomain: process.env.REACT_APP_authDomain,
    databaseURL: process.env.REACT_APP_databaseURL,
    projectId: process.env.REACT_APP_projectId,
    storageBucket: process.env.REACT_APP_storageBucket,
    messagingSenderId: process.env.REACT_APP_messagingSenderId,
    appId: process.env.REACT_APP_appId,
    measurementId: process.env.REACT_APP_measurementId,
};

const app = initializeApp(firebaseConfig);

export default function BasicCard() {

    const [durum, setDurum] = useState('SAFE DRIVING');
    const [sonTespit, setSonTespit] = useState('');

    const changeDateIfUnsafe = () => {
        var today = new Date();
        var date = today.getDate() + '/' + (today.getMonth() + 1) + '/' + today.getFullYear();

        const d = new Date();
        const n = date + '   ' + d.toLocaleTimeString();

        if (durum !== 'SAFE DRIVING') {
            setSonTespit(n);
        }
    };

    useEffect(changeDateIfUnsafe, [durum]);

    useEffect(() => {

        const db = getDatabase();
        const guvenlikDurumuRef = ref(db, 'myData');
        onValue(guvenlikDurumuRef, (snapshot) => {
            const data = snapshot.val();
            setDurum(data['guvenlikDurumu']);
        });
    });

    let color = durum.toLowerCase() === 'safe driving' ? 'green' : 'red';

    return (
        <Card sx={{background: color}}>
            <CardContent style={{
                display: 'flex', flexDirection: 'column', justifyContent: 'space-around', alignItems: 'center',
                fontFamily: 'sans-serif', height: '50vh', width: '50vw'
            }}>
                <Typography variant="h5" component="div" visibility={'visible'}
                            style={{fontSize: '2.5vmax', textAlign: 'center'}}>
                    {durum}
                </Typography>
                <Typography variant="body2" style={{fontSize: '1.8vmax', textAlign: 'center'}}>
                    Last detection date: {sonTespit}
                    <br/>
                </Typography>
            </CardContent>
        </Card>
    );
}