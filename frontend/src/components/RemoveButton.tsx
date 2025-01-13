'use client'
import { Button, Dialog, DialogActions, DialogContent } from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import { FormEvent, PropsWithChildren, useState } from "react";

interface Props extends PropsWithChildren {
    onSubmit: () => void;
}
export const RemoveButton: React.FC<Props> = ({onSubmit}) => {
    const [isOpen, setIsOpen] = useState<boolean>(false);
    return (
        <>
            <Button sx={{ ml: "auto" }} startIcon={<AddIcon />} onClick={() => setIsOpen(true)} variant="contained">
                Usuń
            </Button>
            <Dialog open={isOpen}>
                <DialogContent>
                    Czy na pewno chcesz usunąć
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setIsOpen(false)}>Nie</Button>
                    <Button onClick={onSubmit}>Tak</Button>
                </DialogActions>
            </Dialog>
        </>
    );
};
