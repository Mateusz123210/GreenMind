'use client'
import { Button, Dialog, DialogActions, DialogContent, Stack } from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import { FormEvent, PropsWithChildren, useState } from "react";

interface Props extends PropsWithChildren {
    onSubmit: () => void;
}
export const RemoveButton: React.FC<Props> = ({onSubmit}) => {
    const [isOpen, setIsOpen] = useState<boolean>(false);
    const onYes = () => {
        onSubmit();
        setIsOpen(false)
    }
    return (
        <>
            <Stack direction="row" alignItems="end" px={2} py={0}>
            <Button sx={{ ml: "auto" }} color="error" startIcon={<AddIcon />} onClick={() => setIsOpen(true)} variant="contained">
                Usuń
            </Button>
            </Stack>
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
