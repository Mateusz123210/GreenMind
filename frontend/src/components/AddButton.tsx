"use client";
import { Button, Dialog, DialogContent, DialogTitle } from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import { FormEvent, PropsWithChildren, useState } from "react";

interface Props<T> extends PropsWithChildren {
    onSubmit: (values: T) => void;
}
export const AddButton = <T,>({ onSubmit, children }: Props<T>) => {
    const [isOpen, setIsOpen] = useState<boolean>(false);
    const onSubmitForm = (e: FormEvent<HTMLFormElement>) => {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const data = Object.fromEntries(new FormData(e.nativeEvent.target as any).entries());
        console.log(data);
        e.preventDefault();
        onSubmit(data as T);
    };
    return (
        <>
            <Button
                sx={{ ml: "auto" }}
                startIcon={<AddIcon />}
                onClick={() => setIsOpen(true)}
                variant="contained"
            >
                Dodaj
            </Button>
            <Dialog open={isOpen} onClose={() => setIsOpen(false)}>
                <DialogTitle>Dodaj</DialogTitle>
                <DialogContent>
                    <form onSubmit={onSubmitForm}>
                        {children}
                        <Button type="submit" variant="contained" fullWidth>
                            Zatwierdź
                        </Button>
                    </form>
                </DialogContent>
            </Dialog>
        </>
    );
};
