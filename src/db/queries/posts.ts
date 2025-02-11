import type {Post} from "@prisma/client"
import {db} from "@/db"
import {notFound} from "next/navigation"

export async function fetchPost(): Promise<Post[]> {
    return await db.post.findMany({
        orderBy: [
            {
                updateAt: "desc",
            }
        ],
    })
}


export async function fetchPostById(id: string): Promise<Post | null> {
    const post = await db.post.findFirst({
        where: {
            id
        }
    })

    if (!post) {
        notFound()
    }

    return post
}