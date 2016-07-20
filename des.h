/*****************************************************************************
 * des.h                                                                     *
 *                           Header file for des.c                           *
 *                                                                           *
 *   Written 1995-8 by Cryptography Research (http://www.cryptography.com)   *
 *   Original version by Paul Kocher. Placed in the public domain in 1998.   *
 *  THIS IS UNSUPPORTED FREE SOFTWARE. USE AND DISTRIBUTE AT YOUR OWN RISK.  *
 *                                                                           *
 *  IMPORTANT: U.S. LAW MAY REGULATE THE USE AND/OR EXPORT OF THIS PROGRAM.  *
 *                                                                           *
 *****************************************************************************
 *                                                                           *
 *   REVISION HISTORY:                                                       *
 *                                                                           *
 *   Version 1.0:  Initial release  -- PCK.                                  *
 *   Version 1.1:  Changes and edits for EFF DES Cracker project.            *
 *                                                                           *
 *****************************************************************************/

#ifndef __DES_H
#define __DES_H

#ifndef __cplusplus
typedef char bool;
#endif

void EncryptDES(bool key[64], bool inBlk[64], bool outBlk[64]);
void DecryptDES(bool key[64], bool inBlk[64], bool outBlk[64]);

#endif

