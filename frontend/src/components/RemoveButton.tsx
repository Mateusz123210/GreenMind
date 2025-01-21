'use client'
import { Button, Dialog, DialogActions, DialogContent } from "@mui/material";
import DeleteIcon from '@mui/icons-material/Delete';
import { PropsWithChildren, useState } from "react";

interface Props extends PropsWithChildren {
    onSubmit: () => void;
    absolute?: boolean;
}
export const RemoveButton: React.FC<Props> = ({onSubmit, absolute = false}) => {
    const [isOpen, setIsOpen] = useState<boolean>(false);
    const onYes = () => {
        onSubmit();
        setIsOpen(false)
    }
    return (
        <>
            <Button sx={{ float: "right", m: 1 }} color="error" startIcon={<DeleteIcon />} onClick={() => setIsOpen(true)} variant="outlined">
                Usuń
            </Button>
            <Dialog open={isOpen}>
                <DialogContent>
                    Czy na pewno chcesz usunąć
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setIsOpen(false)} variant="contained">Nie</Button>
                    <Button onClick={onYes} color="error" variant="contained">Tak</Button>
                </DialogActions>
            </Dialog>
        </>
    );
};
