'use client'
import { Button, Dialog, DialogActions, DialogContent, Stack } from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import { FormEvent, PropsWithChildren, useState } from "react";

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
            <Button sx={{ float: "right", m: 1 }} color="error" startIcon={<AddIcon />} onClick={() => setIsOpen(true)} variant="outlined">
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
