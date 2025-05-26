import React, { useState, useEffect } from 'react';
import api from '../utils/axios';
import {
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Paper,
    Button,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    TextField,
    Box,
    Alert,
} from '@mui/material';



export default function BarList() {
    const [bars, setBars] = useState([]);
    const [open, setOpen] = useState(false);
    const [selectedBar, setSelectedBar] = useState(null);
    const [newBar, setNewBar] = useState({
        machine_id: 'MACHINE1',
        lot_id: 'LOT123',
        product_id: 'PRODUCT1',
        recipe_id: 'RECIPE1',
        bar_count: 10,
        time_duration: 30.5,
    });
    const [error, setError] = useState('');

    useEffect(() => {
        fetchBars();
    }, []);

    const fetchBars = async () => {
        try {
            const response = await api.get('/bars');
            setBars(response.data);
            setError('');
        } catch (err) {
            setError('데이터를 불러오는데 실패했습니다: ' + err.message);
        }
    };

    const handleCreate = async () => {
        try {
            const response = await api.post('/bars', newBar);
            fetchBars();
            setOpen(false);
            setError('');
        } catch (err) {
            setError('데이터를 생성하는데 실패했습니다: ' + err.message);
        }
    };

    const handleUpdate = async () => {
        try {
            await api.put(`/bars/${selectedBar.id}`, selectedBar);
            fetchBars();
            setOpen(false);
        } catch (error) {
            setError('Error updating bar: ' + error.message);
        }
    };

    const handleDelete = async (id) => {
        if (window.confirm('정말로 삭제하시겠습니까?')) {
            try {
                await api.delete(`/bars/${id}`);
                fetchBars();
            } catch (error) {
                setError('Error deleting bar: ' + error.message);
            }
        }
    };

    const handleOpenDialog = (bar = null) => {
        if (bar) {
            setSelectedBar({ ...bar });
        } else {
            setSelectedBar(null);
        }
        setOpen(true);
    };

    return (
        <div style={{ padding: '20px' }}>
            <Button
                variant="contained"
                color="primary"
                onClick={handleCreate}
                style={{ marginRight: '8px' }}
            >
                테스트 데이터 생성
            </Button>
            <Button
                variant="contained"
                color="primary"
                onClick={() => handleOpenDialog()}
            >
                Bar 추가
            </Button>
            {error && (
                <Alert severity="error" style={{ marginTop: '16px' }}>
                    {error}
                </Alert>
            )}
            <TableContainer component={Paper} style={{ marginTop: '20px' }}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Machine ID</TableCell>
                            <TableCell>Lot ID</TableCell>
                            <TableCell>Product ID</TableCell>
                            <TableCell>Recipe ID</TableCell>
                            <TableCell>Bar Count</TableCell>
                            <TableCell>Time Duration</TableCell>
                            <TableCell>Actions</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {bars.map((bar) => (
                            <TableRow key={bar.id}>
                                <TableCell>{bar.machine_id}</TableCell>
                                <TableCell>{bar.lot_id}</TableCell>
                                <TableCell>{bar.product_id}</TableCell>
                                <TableCell>{bar.recipe_id}</TableCell>
                                <TableCell>{bar.bar_count}</TableCell>
                                <TableCell>{bar.time_duration}</TableCell>
                                <TableCell>
                                    <Button
                                        variant="outlined"
                                        size="small"
                                        onClick={() => handleOpenDialog(bar)}
                                    >
                                        수정
                                    </Button>
                                    <Button
                                        variant="outlined"
                                        color="error"
                                        size="small"
                                        onClick={() => handleDelete(bar.id)}
                                        style={{ marginLeft: '8px' }}
                                    >
                                        삭제
                                    </Button>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>

            <Dialog open={open} onClose={() => setOpen(false)}>
                <DialogTitle>
                    {selectedBar ? 'Bar 수정' : 'Bar 추가'}
                </DialogTitle>
                <DialogContent>
                    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
                        <TextField
                            label="Machine ID"
                            value={selectedBar ? selectedBar.machine_id : newBar.machine_id}
                            onChange={(e) => {
                                if (selectedBar) {
                                    setSelectedBar({ ...selectedBar, machine_id: e.target.value });
                                } else {
                                    setNewBar({ ...newBar, machine_id: e.target.value });
                                }
                            }}
                        />
                        <TextField
                            label="Lot ID"
                            value={selectedBar ? selectedBar.lot_id : newBar.lot_id}
                            onChange={(e) => {
                                if (selectedBar) {
                                    setSelectedBar({ ...selectedBar, lot_id: e.target.value });
                                } else {
                                    setNewBar({ ...newBar, lot_id: e.target.value });
                                }
                            }}
                        />
                        <TextField
                            label="Product ID"
                            value={selectedBar ? selectedBar.product_id : newBar.product_id}
                            onChange={(e) => {
                                if (selectedBar) {
                                    setSelectedBar({ ...selectedBar, product_id: e.target.value });
                                } else {
                                    setNewBar({ ...newBar, product_id: e.target.value });
                                }
                            }}
                        />
                        <TextField
                            label="Recipe ID"
                            value={selectedBar ? selectedBar.recipe_id : newBar.recipe_id}
                            onChange={(e) => {
                                if (selectedBar) {
                                    setSelectedBar({ ...selectedBar, recipe_id: e.target.value });
                                } else {
                                    setNewBar({ ...newBar, recipe_id: e.target.value });
                                }
                            }}
                        />
                        <TextField
                            label="Bar Count"
                            type="number"
                            value={selectedBar ? selectedBar.bar_count : newBar.bar_count}
                            onChange={(e) => {
                                if (selectedBar) {
                                    setSelectedBar({ ...selectedBar, bar_count: parseInt(e.target.value) });
                                } else {
                                    setNewBar({ ...newBar, bar_count: parseInt(e.target.value) });
                                }
                            }}
                        />
                        <TextField
                            label="Time Duration"
                            type="number"
                            value={selectedBar ? selectedBar.time_duration : newBar.time_duration}
                            onChange={(e) => {
                                if (selectedBar) {
                                    setSelectedBar({ ...selectedBar, time_duration: parseFloat(e.target.value) });
                                } else {
                                    setNewBar({ ...newBar, time_duration: parseFloat(e.target.value) });
                                }
                            }}
                        />
                    </Box>
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setOpen(false)}>취소</Button>
                    <Button
                        onClick={selectedBar ? handleUpdate : handleCreate}
                        variant="contained"
                        color="primary"
                    >
                        {selectedBar ? '수정' : '추가'}
                    </Button>
                </DialogActions>
            </Dialog>
        </div>
    );
}
